# Arquivo: simulador_gateway.py

import requests
import random
import math
from datetime import datetime

# Endpoint da API
GATEWAY_API_URL = "http://18.223.171.40:8181/cxf/m2fot/fot-gateway"

# Fabricantes e soluções simuladas
GATEWAY_MANUFACTURERS = [
    "Bosch IoT Suite", "Cisco IoT", "Siemens Mindsphere",
    "Amazon AWS IoT", "Google Cloud IoT", "IBM Watson IoT", "Intel IoT", "Microsoft Azure IoT",
    "Schneider Electric EcoStruxure", "GE Digital Predix", "Huawei OceanConnect IoT", "Samsung Artik",
    "Honeywell Connected Enterprise", "PTC ThingWorx", "Sigfox", "Telenor Connexion", "Zebra Technologies",
    "NXP Semiconductors", "STMicroelectronics", "u-blox"
]

SMART_SOLUTIONS = [
    "smart traffic", "smart parking", "structural health",
    "water quality", "traffic congestion", "smart lighting", "air pollution", "forest fire detection"
]

def gerar_coordenada_aleatoria(centro_lat, centro_lon, raio_km):
    """Gera coordenadas geográficas aleatórias dentro de um raio"""
    raio_terra_km = 6371.0
    delta_lat = (raio_km / raio_terra_km) * (180 / math.pi)
    delta_lon = delta_lat / math.cos(centro_lat * math.pi / 180)

    lat = centro_lat + random.uniform(-delta_lat, delta_lat)
    lon = centro_lon + random.uniform(-delta_lon, delta_lon)

    return {"latitude": lat, "longitude": lon}

def gerar_mac():
    """Gera um endereço MAC aleatório"""
    return ":".join(str(random.randint(0, 31)) for _ in range(6))

def gerar_ip():
    """Gera um endereço IP aleatório"""
    return ".".join(str(random.randint(0, 191)) for _ in range(4))

def gerar_gateway(central_lat, central_lon, raio_km):
    """Gera um gateway simulado"""
    agora = datetime.now()
    return {
        "mac": gerar_mac(),
        "ip": gerar_ip(),
        "manufacturer": random.choice(GATEWAY_MANUFACTURERS),
        "hostName": f"GT{random.randint(0, 191)}",
        "status": True,
        "date": {
            "year": agora.year,
            "month": agora.month,
            "dayOfMonth": agora.day,
            "hourOfDay": agora.hour,
            "minute": agora.minute,
            "second": agora.second
        },
        "solution": random.choice(SMART_SOLUTIONS),
        "coordinates": gerar_coordenada_aleatoria(central_lat, central_lon, raio_km)
    }

def enviar_gateway_para_api(gateway):
    """Envia um gateway gerado para a API"""
    try:
        resposta = requests.post(GATEWAY_API_URL, json=gateway)
        resposta.raise_for_status()
        print(f"✅ Gateway enviado: {gateway['mac']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar gateway {gateway['mac']}: {e}")

def gerar_gateways_simulados(total_gateways, central_lat, central_lon, raio_km):
    """Gera e envia gateways simulados"""
    print(f"\n🚀 Gerando {total_gateways} gateways simulados...")
    gateways = [gerar_gateway(central_lat, central_lon, raio_km) for _ in range(total_gateways)]

    for gateway in gateways:
        enviar_gateway_para_api(gateway)

    print("✔️ Inserção de gateways concluída.")

def obter_macs():
    """Faz uma requisição GET à API e retorna uma lista com os endereços MAC dos gateways."""
    macs = []

    try:
        resposta = requests.get(GATEWAY_API_URL)
        resposta.raise_for_status()

        dispositivos = resposta.json()

        if not isinstance(dispositivos, list):
            print("⚠️ A resposta da API não é uma lista de dispositivos.")
            return []

        for d in dispositivos:
            mac = d.get("mac")
            if mac:
                macs.append(mac)

        return macs

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar API de gateways: {e}")
        return []
