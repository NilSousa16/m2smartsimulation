from fastapi import FastAPI
from app.routers import gateway, device, gateway_status, status_device

app = FastAPI(
    title="IoT Smart Simulation API",
    description="API for simulating IoT Gateways and Devices for Smart Cities",
    version="1.0.0",
)

app.include_router(gateway.router, prefix="/gateway", tags=["Gateway"])
app.include_router(device.router, prefix="/device", tags=["Device"])
app.include_router(gateway_status.router, prefix="/status-gateway", tags=["Gateways Status"])
app.include_router(status_device.router, prefix="/status-device", tags=["Device Status"])

@app.get("/")
def read_root():
    return {"message": "IoT Simulator API is running"}

