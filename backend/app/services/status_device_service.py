# app/services/status_device_service.py

import requests
import random
import time
from datetime import datetime
from typing import Dict
import copy

from app.config import DEVICE_API_URL, DEVICE_STATUS_API_URL

# Modos de operação (histórico)
OPERATION_MODES = ["operational", "test", "disabled", "maintenance"]

# Controle do loop
device_status_loop_running = True

# Memória local para evitar PUTs desnecessários
_last_known_status: Dict[str, bool] = {}


def get_devices():
    try:
        response = requests.get(DEVICE_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching devices: {e}")
        return []


def _now_date_dict():
    now = datetime.now()
    return {
        "year": now.year,
        "month": now.month,
        "dayOfMonth": now.day,
        "hourOfDay": now.hour,
        "minute": now.minute,
        "second": now.second
    }


def generate_device_status(device_id, timestamp):
    return {
        "idDevice": device_id,
        "date": {
            "year": timestamp.year,
            "month": timestamp.month,
            "dayOfMonth": timestamp.day,
            "hourOfDay": timestamp.hour,
            "minute": timestamp.minute,
            "second": timestamp.second
        },
        "situation": random.choice(OPERATION_MODES)
    }


def send_device_status_to_api(status_data):
    try:
        response = requests.post(DEVICE_STATUS_API_URL, json=status_data, timeout=10)
        response.raise_for_status()
        print(f"✅ Device status sent: {status_data['idDevice']} @ {status_data['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending device status: {e}")


def _put_full_device_payload(updated_device: dict) -> bool:
    """
    Envia o payload COMPLETO do device via PUT para atualizar o campo booleano 'status'.
    Mantém a estrutura retornada pelo GET e só altera 'status' e 'date'.
    Retorna True/False conforme sucesso da operação.
    """
    try:
        resp = requests.put(DEVICE_API_URL, json=updated_device, timeout=10)
        resp.raise_for_status()
        print(f"🔄 Device {updated_device.get('id')} updated via PUT (status={updated_device.get('status')}).")
        return True
    except requests.RequestException as e:
        print(f"❌ Error updating device {updated_device.get('id')}: {e}")
        return False


def maybe_update_device_power_state(device: dict, prob_down: float = 0.12, prob_up: float = 0.25) -> dict:
    """
    Decide aleatoriamente se atualiza o booleano 'status' do cadastro do device (via PUT) e
    RETORNA o device (atualizado ou original).

    - Se o device está ON (True): com prob_down, desliga (False).
    - Se está OFF (False): com prob_up, liga (True).

    Sempre que mudar, envia o JSON completo (como veio do GET) com 'status' e 'date' atualizados.
    """
    device_id = device.get("id")
    if not device_id:
        return device

    current_status = bool(device.get("status", True))
    prev_mem = _last_known_status.get(device_id, current_status)

    new_status = current_status
    if current_status and random.random() < prob_down:
        new_status = False
    elif not current_status and random.random() < prob_up:
        new_status = True

    # Evita PUT se nada mudou
    if new_status == current_status:
        _last_known_status[device_id] = current_status
        return device

    # Monta payload completo alterando apenas status e date
    payload = copy.deepcopy(device)
    payload["status"] = new_status
    payload["date"] = _now_date_dict()

    # IMPORTANTE: mantenha 'gateway' exatamente como o GET retornou.
    if _put_full_device_payload(payload):
        _last_known_status[device_id] = new_status
        return payload  # devolve o device atualizado para uso imediato no loop
    else:
        # PUT falhou; mantemos o original
        _last_known_status[device_id] = current_status
        return device


def start_device_status_loop(interval_seconds: int = 5):
    global device_status_loop_running
    device_status_loop_running = True

    print(f"\n⏳ Starting device status loop every {interval_seconds} seconds...")

    try:
        while device_status_loop_running:
            devices = get_devices()
            if not devices:
                print("⚠️ No devices found.")
                time.sleep(interval_seconds)
                continue

            # Timestamp único por rodada (como no backend Java)
            now = datetime.now()

            for device in devices:
                if not device_status_loop_running:
                    break

                device_id = device.get("id")
                if not device_id:
                    continue

                # 1) (Novo) chance de alternar status ON/OFF e persistir via PUT — retorna o device (atualizado ou não)
                device = maybe_update_device_power_state(device)

                # 2) Só envia status histórico se o device estiver ON (status=True)
                if bool(device.get("status", True)):
                    status = generate_device_status(device_id, now)
                    send_device_status_to_api(status)
                else:
                    # opcional: debug curto
                    # print(f"⏸️ Skipping status for OFF device {device_id}")
                    pass

            time.sleep(interval_seconds)

    except Exception as e:
        print(f"❌ Error during device status loop: {e}")


def stop_device_status_loop():
    global device_status_loop_running
    device_status_loop_running = False
    print("🛑 Device status loop stopped.")


def get_device_statuses():
    """Retrieve list of device statuses from the API."""
    try:
        response = requests.get(DEVICE_STATUS_API_URL, timeout=10)
        response.raise_for_status()

        statuses = response.json()

        if not isinstance(statuses, list):
            print("⚠️ API response is not a list of device statuses.")
            return []

        print(f"✅ Retrieved {len(statuses)} device statuses.")
        return statuses

    except requests.exceptions.Timeout:
        print("⏳ Timeout error while fetching device statuses.")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error while fetching device statuses.")
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP error while fetching device statuses: {http_err} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Unexpected error fetching device statuses: {e}")

    return []
