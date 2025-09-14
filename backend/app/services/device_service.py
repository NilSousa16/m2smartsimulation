import requests
import random
import uuid
import math
from datetime import datetime
from typing import List, Dict, Any, Tuple
from app.config import GATEWAY_API_URL
from app.config import DEVICE_API_URL

# Device Types
DEVICE_TYPES = [
    {"name": "temperature sensor", "type": "sensor"},
    {"name": "humidity sensor", "type": "sensor"},
    {"name": "air quality sensor", "type": "sensor"},
    {"name": "noise level sensor", "type": "sensor"},
    {"name": "CO2 sensor", "type": "sensor"},
    {"name": "traffic flow sensor", "type": "sensor"},
    {"name": "parking occupancy sensor", "type": "sensor"},
    {"name": "smart energy meter", "type": "sensor"},
    {"name": "waste bin fill-level sensor", "type": "sensor"},
    {"name": "flood detection sensor", "type": "sensor"},
    {"name": "rain gauge sensor", "type": "sensor"},
    {"name": "UV radiation sensor", "type": "sensor"},
    {"name": "wind speed sensor", "type": "sensor"},
    {"name": "motion detector (public spaces)", "type": "sensor"},
    {"name": "camera (CCTV)", "type": "sensor"},

    {"name": "smart traffic light controller", "type": "actuator"},
    {"name": "smart streetlight", "type": "actuator"},
    {"name": "public irrigation valve", "type": "actuator"},
    {"name": "electric vehicle charging station", "type": "actuator"},
    {"name": "automated waste compactor", "type": "actuator"},
    {"name": "environmental alarm system", "type": "actuator"},
    {"name": "automatic barrier gate", "type": "actuator"},
    {"name": "dynamic road sign", "type": "actuator"},
    {"name": "smart ventilation system", "type": "actuator"},
    {"name": "drainage control valve", "type": "actuator"},
    {"name": "emergency siren", "type": "actuator"},
    {"name": "smart building HVAC control", "type": "actuator"},
    {"name": "automated street cleaning system", "type": "actuator"},
    {"name": "public display panel", "type": "actuator"},
    {"name": "smart crosswalk signal", "type": "actuator"}
]


def fetch_gateways() -> List[Dict[str, Any]]:
    try:
        response = requests.get(GATEWAY_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching gateways: {e}")
        return []


def fetch_devices() -> List[Dict[str, Any]]:
    try:
        response = requests.get(DEVICE_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching devices: {e}")
        return []


def generate_random_coordinate(center_lat: float, center_lon: float, radius_km: float) -> Dict[str, float]:
    earth_radius_km = 6371.0
    delta_lat = (radius_km / earth_radius_km) * (180 / math.pi)
    delta_lon = delta_lat / math.cos(center_lat * math.pi / 180)
    lat = center_lat + random.uniform(-delta_lat, delta_lat)
    lon = center_lon + random.uniform(-delta_lon, delta_lon)
    return {"latitude": lat, "longitude": lon}


def generate_device(gateway: Dict[str, Any], radius_km: float) -> Dict[str, Any] | None:
    device_type = random.choice(DEVICE_TYPES)
    now = datetime.now()
    coordinates_gateway = gateway.get("coordinates")

    if not coordinates_gateway:
        print(f"⚠️ Gateway {gateway.get('mac')} has no valid coordinates. Skipping.")
        return None

    coordinates = generate_random_coordinate(
        coordinates_gateway["latitude"], coordinates_gateway["longitude"], radius_km
    )

    return {
        "id": str(uuid.uuid4()),
        "coordinates": coordinates,
        "description": "DTM",
        "typeDevice": device_type["name"],
        "category": device_type["type"],
        "status": random.choice([True, False]),
        "date": {
            "year": now.year,
            "month": now.month,
            "dayOfMonth": now.day,
            "hourOfDay": now.hour,
            "minute": now.minute,
            "second": now.second,
        },
        "gateway": {
            "mac": gateway["mac"]
        }
    }


def send_device_to_api(device: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        response = requests.post(DEVICE_API_URL, json=device)
        response.raise_for_status()
        print(f"✅ Device sent: {device['id']}")
        return True, f"Device {device['id']} sent successfully"
    except requests.RequestException as e:
        print(f"❌ Error sending device {device['id']}: {e}")
        return False, str(e)


def generate_simulated_devices(total_devices: int, radius_km: float) -> Tuple[int, int]:
    print(f"\n🔧 Generating {total_devices} simulated devices...")
    gateways = fetch_gateways()

    if not gateways:
        print("⚠️ No gateways found. Aborting device generation.")
        return 0, total_devices

    success_count = 0
    failure_count = 0

    for _ in range(total_devices):
        gateway = random.choice(gateways)
        device = generate_device(gateway, radius_km)
        if device:
            success, _ = send_device_to_api(device)
            if success:
                success_count += 1
            else:
                failure_count += 1
        else:
            failure_count += 1

    print(f"✔️ Device insertion completed. Success: {success_count}, Failed: {failure_count}")
    return success_count, failure_count

def get_device_ids() -> List[str]:
    """Retrieve list of device IDs from the API."""
    devices = fetch_devices()

    if not devices:
        print("⚠️ No devices found.")
        return []

    ids = [device.get("id") for device in devices if device.get("id")]
    return ids

def update_device(device_payload: dict):
    """
    Sends a full device JSON via PUT to the external API.
    """
    try:
        # A API de vocês recebe PUT no mesmo endpoint do POST
        resp = requests.put(DEVICE_API_URL, json=device_payload, timeout=10)
        resp.raise_for_status()
        return True, "OK"
    except requests.RequestException as e:
        return False, str(e)