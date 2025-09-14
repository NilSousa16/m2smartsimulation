# 🧠 Backend - M2SmartSimulation

Este repositório contém o backend da aplicação **M2SmartSimulation**, desenvolvido em **Python** com o framework **FastAPI**. Ele atua como intermediador entre o frontend e os serviços externos responsáveis pela gestão de dispositivos e gateways em ambientes IoT.

---

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── main.py               # Ponto de entrada da API FastAPI
│   ├── config.py             # Configurações e carregamento do .env
│   ├── routers/              # Rotas/endpoints REST
│   ├── services/             # Lógica de comunicação com APIs externas
│   └── models/schemas.py     # Modelos de dados com Pydantic
├── .env                      # Variáveis de ambiente para URLs das APIs externas
├── README.md
```

---

## ⚙️ Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) - servidor ASGI
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Requests](https://docs.python-requests.org/)

---

## 🚀 Como executar o backend

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/m2smartsimulation.git
cd m2smartsimulation/backend
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python3 -m venv venv
source venv/bin/activate     # Linux/macOS
# ou
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install fastapi uvicorn python-dotenv requests
```

### 4. Configure o arquivo `.env`

Verifique se o arquivo `.env` está presente com os seguintes valores (URLs podem ser ajustadas conforme o ambiente):

```env
# .env
GATEWAY_API_URL=http://18.223.171.40:8181/cxf/m2fot/fot-gateway
DEVICE_API_URL=http://18.223.171.40:8181/cxf/m2fot-device/fot-device
GATEWAY_STATUS_API_URL=http://18.223.171.40:8181/cxf/m2fot-status/fot-gateway-status/
DEVICE_STATUS_API_URL=http://18.223.171.40:8181/cxf/m2fot-device-status/fot-device-status/
```

### 5. Execute o servidor

```bash
uvicorn app.main:app --reload
# ou
python -m uvicorn app.main:app --reload
```

### 6. Acesse a documentação da API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testes

> (Este projeto ainda não contém testes automatizados. Sinta-se à vontade para contribuir.)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.