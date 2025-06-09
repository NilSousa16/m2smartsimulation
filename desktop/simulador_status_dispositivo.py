import requests
import random
from datetime import datetime, timedelta

# URL da API
DEVICE_API_URL = "http://18.223.171.40:8181/cxf/m2fot-device/fot-device"
STATUS_API_URL = "http://18.223.171.40:8181/cxf/m2fot-device-status/fot-device-status/"

# Situações possíveis para o status do dispositivo
OPERATION_MODES = ["operational", "test", "disabled", "maintenance"]

def obter_dispositivos():
    """Obtém a lista de dispositivos existentes na API"""
    try:
        resposta = requests.get(DEVICE_API_URL)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter dispositivos: {e}")
        return []

def gerar_status_dispositivo(device_id, timestamp):
    """Gera um registro de status para um dispositivo"""
    return {
        "idDevice": device_id,  # ✅ Corrigido aqui
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

def enviar_status_para_api(status):
    """Envia o status do dispositivo para a API"""
    try:
        resposta = requests.post(STATUS_API_URL, json=status)
        resposta.raise_for_status()
        print(f"✅ Status enviado para o dispositivo {status['idDevice']} @ {status['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar status: {e}")

def gerar_status_simulado_dispositivos(total_status=5):
    """Gera e envia status simulados para todos os dispositivos"""
    dispositivos = obter_dispositivos()
    if not dispositivos:
        print("⚠️ Nenhum dispositivo encontrado.")
        return

    tempo = datetime.now()

    for dispositivo in dispositivos:
        device_id = dispositivo.get("id")
        if not device_id:
            continue

        for _ in range(total_status):
            tempo += timedelta(seconds=1)
            status = gerar_status_dispositivo(device_id, tempo)
            enviar_status_para_api(status)

    print("\n✔️ Inserção de status dos dispositivos concluída.")
