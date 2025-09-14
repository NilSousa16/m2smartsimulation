# app/services/gateway_status_service.py

import requests
import random
import time
from datetime import datetime
from typing import Dict, Any, List

from app.services.gateway_service import get_macs
from app.config import (
    GATEWAY_STATUS_API_URL,
    GATEWAY_API_URL,
    DEVICE_API_URL,
)

# Flag to control loop
status_loop_running = True

# Cache local para evitar PUTs desnecessários no cadastro do gateway
_last_known_gateway_status: Dict[str, bool] = {}

# ✅ NOVO: guarda o status anterior dos devices quando um gateway cai (por MAC do gateway)
# estrutura: { gateway_mac: { device_id: bool_anterior } }
_device_prev_status_by_gateway: Dict[str, Dict[str, bool]] = {}


def generate_status(gateway_mac: str, timestamp: datetime, state: Dict[str, float]) -> Dict[str, Any]:
    """Gera status do gateway com True/False aleatório (50/50) e métricas variando suavemente."""
    active = bool(random.getrandbits(1))  # True/False com 50% de probabilidade

    battery = max(0.0, round(state["baterryLevel"] - random.uniform(0.001, 0.005), 2))
    memory = min(1.0, max(0.0, round(state["usedMemory"] + random.uniform(-0.05, 0.05), 2)))
    cpu = min(1.0, max(0.0, round(state["usedProcessor"] + random.uniform(-0.05, 0.05), 2)))

    return {
        "date": {
            "year": timestamp.year,
            "month": timestamp.month,
            "dayOfMonth": timestamp.day,
            "hourOfDay": timestamp.hour,
            "minute": timestamp.minute,
            "second": timestamp.second
        },
        "gateway": {
            "mac": gateway_mac,
            "status": active
        },
        "baterryLevel": battery,
        "usedMemory": memory,
        "usedProcessor": cpu
    }


def send_status_to_api(status_data: Dict[str, Any]) -> None:
    """Envia o status gerado para a API de histórico."""
    try:
        response = requests.post(GATEWAY_STATUS_API_URL, json=status_data, timeout=10)
        response.raise_for_status()
        print(f"✅ Status sent: {status_data['gateway']['mac']} @ {status_data['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending status: {e}")


def _fetch_gateways_by_mac() -> Dict[str, Dict[str, Any]]:
    """Busca todos os gateways e indexa por MAC (mantendo campos para PUT completo)."""
    try:
        resp = requests.get(GATEWAY_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            print("⚠️ Gateway API did not return a list.")
            return {}
        by_mac = {}
        for gw in data:
            mac = gw.get("mac")
            if mac:
                by_mac[mac] = gw
        return by_mac
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching gateways for PUT: {e}")
        return {}


def _put_gateway(payload: Dict[str, Any]) -> bool:
    """
    Executa o PUT no cadastro do gateway.
    Retorna True em caso de sucesso (200/204), False caso contrário.
    """
    try:
        resp = requests.put(GATEWAY_API_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"🔄 Gateway updated via PUT: {payload.get('mac')} (status={payload.get('status')})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating gateway {payload.get('mac')}: {e}")
        return False


# ---------------------------
#  Cascata para dispositivos
# ---------------------------

def _fetch_devices() -> List[Dict[str, Any]]:
    """Busca a lista completa de dispositivos."""
    try:
        resp = requests.get(DEVICE_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            print("⚠️ Device API did not return a list.")
            return []
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching devices: {e}")
        return []


def _put_device(payload: Dict[str, Any]) -> bool:
    """
    Executa PUT no cadastro do dispositivo com payload COMPLETO.
    Mantém todos os campos e apenas altera 'status' e 'date'.
    """
    try:
        resp = requests.put(DEVICE_API_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"🔄 Device updated via PUT: {payload.get('id')} (status={payload.get('status')})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating device {payload.get('id')}: {e}")
        return False


def _set_all_devices_offline_for_gateway(gateway_mac: str) -> None:
    """
    Força todos os dispositivos vinculados ao gateway (gateway.mac == gateway_mac)
    a ficarem offline (status=False) via PUT (payload completo).
    Também MEMORIZA o status anterior para futura restauração.
    """
    devices = _fetch_devices()
    if not devices:
        print("ℹ️ No devices to cascade offline.")
        return

    # cria o bucket de memória se não existir
    if gateway_mac not in _device_prev_status_by_gateway:
        _device_prev_status_by_gateway[gateway_mac] = {}

    affected = 0
    now = datetime.now()

    for d in devices:
        gw = d.get("gateway") or {}
        gw_mac = gw.get("mac")
        if gw_mac != gateway_mac:
            continue

        dev_id = d.get("id")
        if not dev_id:
            continue

        # memorize previous status only once (if not stored yet)
        if dev_id not in _device_prev_status_by_gateway[gateway_mac]:
            _device_prev_status_by_gateway[gateway_mac][dev_id] = bool(d.get("status", True))

        # Se já está offline, não precisa PUT
        if d.get("status") is False:
            continue

        payload = dict(d)
        payload["status"] = False
        payload["date"] = {
            "year": now.year,
            "month": now.month,
            "dayOfMonth": now.day,
            "hourOfDay": now.hour,
            "minute": now.minute,
            "second": now.second
        }

        if _put_device(payload):
            affected += 1

    print(f"📉 Cascade: {affected} device(s) set to offline for gateway {gateway_mac}.")


def _restore_devices_for_gateway_online(gateway_mac: str) -> None:
    """
    Quando o gateway volta a ficar online, restaura o status dos devices
    para o que estava MEMORIZADO antes da queda. Se não houver memória,
    não altera o device (deixa como está).
    """
    prev_map = _device_prev_status_by_gateway.get(gateway_mac)
    if not prev_map:
        print(f"ℹ️ No previous device states stored for gateway {gateway_mac}. Nothing to restore.")
        return

    devices = _fetch_devices()
    if not devices:
        print("ℹ️ No devices to restore.")
        return

    restored = 0
    now = datetime.now()

    for d in devices:
        gw = d.get("gateway") or {}
        if gw.get("mac") != gateway_mac:
            continue

        dev_id = d.get("id")
        if not dev_id:
            continue

        # Se temos status anterior, usamos; caso contrário, não mexe
        if dev_id not in prev_map:
            continue

        target_status = prev_map[dev_id]
        if d.get("status") == target_status:
            continue  # já está no estado desejado

        payload = dict(d)
        payload["status"] = target_status
        payload["date"] = {
            "year": now.year,
            "month": now.month,
            "dayOfMonth": now.day,
            "hourOfDay": now.hour,
            "minute": now.minute,
            "second": now.second
        }

        if _put_device(payload):
            restored += 1

    # Limpa a memória para esse gateway (evita estados antigos)
    _device_prev_status_by_gateway.pop(gateway_mac, None)
    print(f"📈 Restore: {restored} device(s) restored for gateway {gateway_mac} (online).")


def _maybe_put_gateway_status(mac: str, new_status: bool, gateways_by_mac: Dict[str, Dict[str, Any]]) -> None:
    """
    Atualiza o cadastro do gateway via PUT se o status tiver mudado.
    Em caso de desligamento (False) bem-sucedido, força devices -> offline.
    Em caso de religamento (True) bem-sucedido, restaura devices ao status anterior.
    """
    prev = _last_known_gateway_status.get(mac)
    _last_known_gateway_status[mac] = new_status  # atualiza cache

    if prev is not None and prev == new_status:
        return  # nada mudou

    gw = gateways_by_mac.get(mac)
    if not gw:
        print(f"⚠️ Gateway metadata for MAC {mac} not found. Skipping PUT.")
        return

    payload = {
        "mac": gw.get("mac"),
        "ip": gw.get("ip"),
        "manufacturer": gw.get("manufacturer"),
        "hostName": gw.get("hostName"),
        "solution": gw.get("solution"),
        "coordinates": gw.get("coordinates"),
        "status": new_status  # incluímos o status atualizado
    }

    success = _put_gateway(payload)

    if success:
        if new_status is False:
            _set_all_devices_offline_for_gateway(mac)
        else:
            _restore_devices_for_gateway_online(mac)


def start_gateway_status_loop(interval_seconds: int = 5) -> None:
    """Inicia o loop contínuo de simulação de status dos gateways."""
    global status_loop_running
    status_loop_running = True

    print(f"\n⏳ Starting gateway status loop every {interval_seconds} seconds...")

    macs = get_macs()
    if not macs:
        print("⚠️ No MAC addresses found. Simulation aborted.")
        return

    states = {
        mac: {
            "baterryLevel": round(random.uniform(0.7, 1.0), 2),
            "usedMemory": round(random.uniform(0.2, 0.5), 2),
            "usedProcessor": round(random.uniform(0.2, 0.5), 2)
        }
        for mac in macs
    }

    gateways_by_mac = _fetch_gateways_by_mac()

    try:
        while status_loop_running:
            now = datetime.now()
            for mac in macs:
                current_state = states[mac]

                # 1) Gera status histórico (inclui status aleatório True/False)
                status_obj = generate_status(mac, now, current_state)

                # 2) Envia status para API de histórico
                send_status_to_api(status_obj)

                # 3) Atualiza cadastro via PUT se mudou (e aplica cascata/restore conforme necessário)
                new_status = bool(status_obj["gateway"]["status"])
                _maybe_put_gateway_status(mac, new_status, gateways_by_mac)

                # 4) Persiste variação das métricas locais
                current_state.update({
                    "baterryLevel": status_obj["baterryLevel"],
                    "usedMemory": status_obj["usedMemory"],
                    "usedProcessor": status_obj["usedProcessor"]
                })

            time.sleep(interval_seconds)

    except Exception as e:
        print(f"❌ Error during status loop: {e}")


def stop_gateway_status_loop() -> None:
    """Encerra o loop contínuo."""
    global status_loop_running
    status_loop_running = False
    print("🛑 Gateway status loop stopped.")


def get_gateway_statuses():
    """Retorna lista de status de gateways gravados (se o backend expõe esse endpoint)."""
    try:
        resp = requests.get(GATEWAY_STATUS_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            print("⚠️ API response is not a list of gateway statuses.")
            return []
        print(f"✅ Retrieved {len(data)} gateway statuses.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching gateway statuses: {e}")
        return []
