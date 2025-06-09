from fastapi import APIRouter, Query
from app.services import device_service
from app.models.schemas import DeviceResponseSchema, DeviceIdListResponse

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
