# 🌎 M2SmartSimulation

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI--Backend-green)
![React](https://img.shields.io/badge/React--Frontend-blue)
![License](https://img.shields.io/badge/license-Academic-lightgrey)

---

## 📦 About the Project

**M2SmartSimulation** is a simulation system for **IoT Gateways** and **IoT Devices** designed for Smart Cities scenarios.  
It enables the simulation of:

- Gateway generation with geographic data
- Device generation linked to gateways
- Continuous or manual sending of gateway status
- Continuous or manual sending of device status
- Communication with REST APIs

---

## 🗂️ Project Structure

```plaintext
M2SMARSimulation/
├── backend/    -> FastAPI REST backend for simulation control
├── frontend/   -> React frontend (Web Interface) [Under development or planned]
├── desktop/    -> Legacy Desktop CLI simulator (Python)
├── .gitignore
├── README.md   -> This README
└── requirements.txt (per component if needed)
