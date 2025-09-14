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
```

---

## 🚀 Como Rodar Localmente

### 🔥 Passo 1: Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate     # Windows
```

### 🔥 Passo 2: Instale as dependências

```bash
pip install -r requirements.txt
```

### 🔥 Passo 3: Execute o servidor

```bash
uvicorn app.main:app --reload
```

O backend estará rodando em:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentação interativa automática (Swagger UI):  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)