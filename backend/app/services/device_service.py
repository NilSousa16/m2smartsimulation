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
    {"name": "temperature sensor", "type": "environment"},
    {"name": "humidity sensor", "type": "environment"},
    {"name": "motion detector", "type": "security"},
    {"name": "light sensor", "type": "lighting"},
    {"name": "air quality monitor", "type": "environment"},
    {"name": "camera", "type": "security"},
    {"name": "parking sensor", "type": "mobility"},
    {"name": "noise sensor", "type": "environment"},
    {"name": "flood sensor", "type": "environment"},
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
        "status": True,
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