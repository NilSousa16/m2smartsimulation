# 🔧 IoT Gateways and Devices Simulator for Smart Cities

This project simulates the behavior of **gateways** and **IoT devices** in a smart city. It allows generating simulated data, sending registration and status information for these devices, and simulating continuous data transmission to REST APIs.

## 🚀 Features

- Insert gateways with simulated geographical locations.
- Insert devices associated with gateways.
- Generate simulated gateway status (battery, memory, processor, and online/offline status).
- Generate simulated device status (operational situation).
- Run in continuous loop mode for gateways, devices, or both simultaneously.

---

## 📦 Requirements

- Python 3.8 or higher

---

## 🔗 API Configuration

The simulator is configured to connect to the following APIs:

- **Gateways:**  
`http://<YOUR_IP>:<PORT>/cxf/m2fot/fot-gateway`

- **Gateway Status:**  
`http://<YOUR_IP>:<PORT>/cxf/m2fot-status/fot-gateway-status/`

- **Devices:**  
`http://<YOUR_IP>:<PORT>/cxf/m2fot-device/fot-device`

- **Device Status:**  
`http://<YOUR_IP>:<PORT>/cxf/m2fot-device-status/fot-device-status/`

> ⚙️ You can edit the files `simulador_gateway.py`, `simulador_status.py`, `simulador_dispositivo.py`, and `simulador_status_dispositivo.py` to set a different API endpoint.

---

## 🏗️ Project Structure

| File                               | Description                                             |
| ---------------------------------- | ------------------------------------------------------- |
| `main.py`                          | Main simulator menu                                     |
| `simulador_gateway.py`             | Gateway generation logic                                |
| `simulador_status.py`              | Gateway status generation                               |
| `simulador_status_loop.py`         | Continuous gateway status simulation                    |
| `simulador_dispositivo.py`         | Device generation linked to gateways                    |
| `simulador_status_dispositivo.py`  | Device status generation                                |
| `simulador_status_dispositivo_loop.py` | Continuous device status simulation                   |
| `simulador_loop_geral.py`          | Runs gateway and device status simulation simultaneously |

---

## 🖥️ How to Run

Run the main file:

```bash
python main.py
