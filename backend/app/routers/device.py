from fastapi import APIRouter, Query
from app.services import device_service
from app.models.schemas import DeviceResponseSchema, DeviceIdListResponse
from pydantic import BaseModel

router = APIRouter()


@router.post("/generate", response_model=DeviceResponseSchema)
def generate_devices(
    total: int = Query(1, description="Number of devices to generate"),
    radius_km: float = Query(1.0, description="Radius around the gateway in km"),
):
    """
    Generate and send simulated devices to the API.
    """
    success_count = device_service.generate_simulated_devices(total, radius_km)

    if success_count == total:
        return {"message": f"✅ {success_count} devices generated successfully."}
    elif success_count == 0:
        return {"message": "❌ Failed to generate any devices. Check the API or network connection."}
    else:
        return {
            "message": f"⚠️ Only {success_count} out of {total} devices were generated successfully."
        }


@router.get("/devices", response_model=DeviceIdListResponse)
def list_device_ids():
    """
    Retrieve list of device IDs from the API.
    """
    ids = device_service.get_device_ids()

    if ids is None:
        return {
            "device_ids": [],
            "message": "❌ Failed to retrieve device IDs. API may be offline."
        }
    elif len(ids) == 0:
        return {
            "device_ids": [],
            "message": "⚠️ No devices found."
        }
    else:
        return {
            "device_ids": ids,
            "message": f"✅ {len(ids)} device IDs retrieved successfully."
        }
# ----------------------------------------------------------
# 🆕 Rota PUT - Atualizar dispositivo (status ou completo)
# ----------------------------------------------------------

# MODELOS Pydantic para a requisição PUT
class Coordinates(BaseModel):
    latitude: float
    longitude: float

class Date(BaseModel):
    year: int
    month: int
    dayOfMonth: int
    hourOfDay: int
    minute: int
    second: int

class GatewayInfo(BaseModel):
    mac: str
    ip: str
    manufacturer: str
    hostName: str
    status: bool
    date: Date
    solution: str
    coordinates: Coordinates

class DeviceUpdate(BaseModel):
    id: str
    coordinates: Coordinates
    description: str
    typeDevice: str
    category: str
    status: bool
    date: Date
    gateway: GatewayInfo

@router.put("/update")
def update_device(device: DeviceUpdate):
    """
    Atualiza completamente um dispositivo IoT no serviço remoto.
    """
    try:
        response = requests.put(
            DEVICE_API_URL,
            json=device.dict()
        )
        response.raise_for_status()
        return {"message": f"✅ Dispositivo {device.id} atualizado com sucesso!"}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar dispositivo: {e}")