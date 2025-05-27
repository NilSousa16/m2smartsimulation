import requests
import random
import uuid
import math
from datetime import datetime

GATEWAY_API_URL = "http://18.223.171.40:8181/cxf/m2fot/fot-gateway"
DEVICE_API_URL = "http://18.223.171.40:8181/cxf/m2fot-device/fot-device"

DEVICE_TYPES = [
    {"name": "temperature sensor", "type": "environment"},
    {"name": "humidity sensor", "type": "environment"},
    {"name": "motion detector", "type": "security"},
    {"name": "light sensor", "type": "lighting"},
    {"name": "air quality monitor", "type": "environment"},
    {"name": "camera", "type": "security"},
    {"name": "parking sensor", "type": "mobility"},
    {"name": "noise sensor", "type": "environment"},
    {"name": "flood sensor", "type": "environment"}
]

def obter_gateways():
    try:
        resposta = requests.get(GATEWAY_API_URL)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter gateways: {e}")
        return []

def gerar_coordenada_aleatoria(centro_lat, centro_lon, raio_km):
    raio_terra_km = 6371.0
    delta_lat = (raio_km / raio_terra_km) * (180 / math.pi)
    delta_lon = delta_lat / math.cos(centro_lat * math.pi / 180)
    lat = centro_lat + random.uniform(-delta_lat, delta_lat)
    lon = centro_lon + random.uniform(-delta_lon, delta_lon)
    return {"latitude": lat, "longitude": lon}

def gerar_dispositivo(gateway, raio_km):
    tipo = random.choice(DEVICE_TYPES)
    agora = datetime.now()
    coordenadas_gateway = gateway.get("coordinates")

    if coordenadas_gateway is None:
        print(f"⚠️ Gateway {gateway.get('mac')} não possui coordenadas válidas. Pulando.")
        return None

    coordenadas = gerar_coordenada_aleatoria(
        coordenadas_gateway["latitude"], coordenadas_gateway["longitude"], raio_km
    )

    return {
        "id": str(uuid.uuid4()),
        "coordinates": coordenadas,
        "description": "DTM",
        "typeDevice": tipo["name"],
        "category": tipo["type"],
        "status": True,
        "date": {
            "year": agora.year,
            "month": agora.month,
            "dayOfMonth": agora.day,
            "hourOfDay": agora.hour,
            "minute": agora.minute,
            "second": agora.second
        },
        "gateway": {
            "mac": gateway["mac"]
        }
    }

def enviar_dispositivo_para_api(dispositivo):
    try:
        resposta = requests.post(DEVICE_API_URL, json=dispositivo)
        resposta.raise_for_status()
        print(f"✅ Dispositivo enviado: {dispositivo['id']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar dispositivo {dispositivo['id']}: {e}")

def gerar_dispositivos_simulados(total_dispositivos, raio_km):
    print(f"\n🔧 Gerando {total_dispositivos} dispositivos simulados...")
    gateways = obter_gateways()
    if not gateways:
        print("⚠️ Nenhum gateway encontrado. Abortando geração de dispositivos.")
        return

    for _ in range(total_dispositivos):
        gateway = random.choice(gateways)
        dispositivo = gerar_dispositivo(gateway, raio_km)
        if dispositivo:
            enviar_dispositivo_para_api(dispositivo)

    print("✔️ Inserção de dispositivos concluída.")
