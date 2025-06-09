import requests
import random
import math
from datetime import datetime
from app.config import GATEWAY_API_URL

# Manufacturers and Solutions
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


def generate_random_coordinate(center_lat, center_lon, radius_km):
    """Generate random geographic coordinates within a radius."""
    earth_radius_km = 6371.0
    delta_lat = (radius_km / earth_radius_km) * (180 / math.pi)
    delta_lon = delta_lat / math.cos(center_lat * math.pi / 180)

    lat = center_lat + random.uniform(-delta_lat, delta_lat)
    lon = center_lon + random.uniform(-delta_lon, delta_lon)

    return {"latitude": lat, "longitude": lon}


def generate_mac():
    """Generate a random MAC address."""
    return ":".join(str(random.randint(0, 31)) for _ in range(6))


def generate_ip():
    """Generate a random IP address."""
    return ".".join(str(random.randint(0, 191)) for _ in range(4))


def generate_gateway(center_lat, center_lon, radius_km):
    """Generate a simulated gateway."""
    now = datetime.now()
    return {
        "mac": generate_mac(),
        "ip": generate_ip(),
        "manufacturer": random.choice(GATEWAY_MANUFACTURERS),
        "hostName": f"GT{random.randint(0, 191)}",
        "status": True,
        "date": {
            "year": now.year,
            "month": now.month,
            "dayOfMonth": now.day,
            "hourOfDay": now.hour,
            "minute": now.minute,
            "second": now.second
        },
        "solution": random.choice(SMART_SOLUTIONS),
        "coordinates": generate_random_coordinate(center_lat, center_lon, radius_km)
    }


def send_gateway_to_api(gateway: dict):
    """Send a generated gateway to the API."""
    try:
        response = requests.post(GATEWAY_API_URL, json=gateway, timeout=10)
        response.raise_for_status()
        print(f"✅ Gateway sent: {gateway['mac']}")
        return True
    except requests.exceptions.Timeout:
        print(f"⏳ Timeout error sending gateway {gateway['mac']}. API might be down or too slow.")
    except requests.exceptions.ConnectionError:
        print(f"🔌 Connection error sending gateway {gateway['mac']}. Check network or API server.")
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP error sending gateway {gateway['mac']}: {http_err} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Unexpected error sending gateway {gateway['mac']}: {e}")
    return False


def generate_simulated_gateways(total_gateways: int, center_lat: float, center_lon: float, radius_km: float) -> int:
    """Generate and send simulated gateways. Returns number of successful sends."""
    print(f"\n🚀 Generating {total_gateways} simulated gateways...")
    gateways = [generate_gateway(center_lat, center_lon, radius_km) for _ in range(total_gateways)]

    success_count = 0
    for gateway in gateways:
        success = send_gateway_to_api(gateway)
        if success:
            success_count += 1
        else:
            print(f"❌ Failed to send gateway {gateway['mac']}")

    print(f"✔️ Gateway generation process completed. {success_count}/{total_gateways} successful.")
    return success_count


def get_macs():
    """Retrieve MAC addresses from API."""
    macs = []

    try:
        response = requests.get(GATEWAY_API_URL, timeout=10)
        response.raise_for_status()

        devices = response.json()

        if not isinstance(devices, list):
            print("⚠️ API response is not a list of devices.")
            return []

        for device in devices:
            mac = device.get("mac")
            if mac:
                macs.append(mac)

        return macs

    except requests.exceptions.Timeout:
        print("⏳ Timeout error while fetching MAC addresses.")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error while fetching MAC addresses. Check API or network.")
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP error: {http_err} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Unexpected error fetching MAC addresses: {e}")

    return []
