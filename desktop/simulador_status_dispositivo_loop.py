import requests
import random
import time
from datetime import datetime
from requests.exceptions import RequestException

# URLs da API
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
    except RequestException as e:
        print(f"❌ Erro ao obter dispositivos: {e}")
        return []

def gerar_status_dispositivo(device_id):
    """Gera um registro de status para um dispositivo"""
    agora = datetime.now()
    return {
        "idDevice": device_id,
        "date": {
            "year": agora.year,
            "month": agora.month,
            "dayOfMonth": agora.day,
            "hourOfDay": agora.hour,
            "minute": agora.minute,
            "second": agora.second
        },
        "situation": random.choice(OPERATION_MODES)
    }

def enviar_status_para_api(status):
    """Envia o status do dispositivo para a API"""
    try:
        resposta = requests.post(STATUS_API_URL, json=status)
        resposta.raise_for_status()
        print(f"✅ Status enviado para o dispositivo {status['idDevice']} @ {status['date']}")
    except RequestException as e:
        print(f"❌ Erro ao enviar status do dispositivo {status['idDevice']}: {e}")

def iniciar_simulacao_status_dispositivo_em_loop(intervalo):
    """Executa a geração de status dos dispositivos em loop"""
    dispositivos = obter_dispositivos()
    if not dispositivos:
        print("⚠️ Nenhum dispositivo encontrado. Encerrando simulação.")
        return

    print("\n🚀 Iniciando geração contínua de status dos dispositivos...")
    print("🛑 Pressione Ctrl + C para interromper.\n")

    try:
        while True:
            for dispositivo in dispositivos:
                device_id = dispositivo.get("id")
                if not device_id:
                    continue

                status = gerar_status_dispositivo(device_id)
                enviar_status_para_api(status)

            time.sleep(intervalo)

    except KeyboardInterrupt:
        print("\n🛑 Simulação de status dos dispositivos interrompida pelo usuário.")
