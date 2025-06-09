# services/status_service.py

import requests
import random
import time
from datetime import datetime

from app.services.gateway_service import get_macs

from app.config import GATEWAY_STATUS_API_URL

# Flag to control loop
status_loop_running = True


def generate_status(gateway_mac, timestamp, state):
    """Generate status for a given gateway."""
    active = random.random() > 0.1  # 90% chance of being active

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


def send_status_to_api(status_data):
    """Send the generated status to the API."""
    try:
        response = requests.post(GATEWAY_STATUS_API_URL, json=status_data)
        response.raise_for_status()
        print(f"✅ Status sent: {status_data['gateway']['mac']} @ {status_data['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending status: {e}")


def start_gateway_status_loop(interval_seconds: int = 5):
    """Start the continuous simulation loop of gateway status."""
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

    try:
        while status_loop_running:
            now = datetime.now()
            for mac in macs:
                current_state = states[mac]
                status = generate_status(mac, now, current_state)
                send_status_to_api(status)

                current_state.update({
                    "baterryLevel": status["baterryLevel"],
                    "usedMemory": status["usedMemory"],
                    "usedProcessor": status["usedProcessor"]
                })

            time.sleep(interval_seconds)

    except Exception as e:
        print(f"❌ Error during status loop: {e}")


def stop_gateway_status_loop():
    """Stop the continuous simulation loop."""
    global status_loop_running
    status_loop_running = False
    print("🛑 Gateway status loop stopped.")

def get_gateway_statuses():
    """Retrieve list of gateway statuses from the API."""
    try:
        response = requests.get(GATEWAY_STATUS_API_URL, timeout=10)
        response.raise_for_status()

        statuses = response.json()

        if not isinstance(statuses, list):
            print("⚠️ API response is not a list of gateway statuses.")
            return []

        print(f"✅ Retrieved {len(statuses)} gateway statuses.")
        return statuses

    except requests.exceptions.Timeout:
        print("⏳ Timeout error while fetching gateway statuses.")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error while fetching gateway statuses.")
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP error while fetching gateway statuses: {http_err} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Unexpected error fetching gateway statuses: {e}")

    return []
