import requests
import random
import time
from datetime import datetime

from app.config import DEVICE_API_URL
from app.config import DEVICE_STATUS_API_URL

# Operation Mode
OPERATION_MODES = ["operational", "test", "disabled", "maintenance"]

# Loop control
device_status_loop_running = True


def get_devices():
    try:
        response = requests.get(DEVICE_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching devices: {e}")
        return []


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
        response = requests.post(STATUS_API_URL, json=status_data)
        response.raise_for_status()
        print(f"✅ Device status sent: {status_data['idDevice']} @ {status_data['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending device status: {e}")


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

            now = datetime.now()

            for device in devices:
                if not device_status_loop_running:
                    break

                device_id = device.get("id")
                if device_id:
                    status = generate_device_status(device_id, now)
                    send_device_status_to_api(status)

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
        response = requests.get(STATUS_API_URL, timeout=10)
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
