from fastapi import APIRouter, Query
from typing import Optional
from app.services import gateway_service
from app.models.schemas import GatewayResponseSchema, GatewayMacListResponse


router = APIRouter()


@router.post("/generate", response_model=GatewayResponseSchema)
def generate_gateways(
    total: int = Query(1, description="Number of gateways to generate"),
    center_lat: float = Query(-13.005, description="Latitude for center point"),
    center_lon: float = Query(-38.516, description="Longitude for center point"),
    radius_km: float = Query(1.0, description="Radius in kilometers"),
):
    """
    Generate and send simulated gateways to the API.
    """
    success_count = gateway_service.generate_simulated_gateways(
        total, center_lat, center_lon, radius_km
    )

    if success_count == total:
        message = f"✅ {success_count} gateways generated successfully."
    elif success_count == 0:
        message = "❌ Failed to generate any gateways. Check the API or network connection."
    else:
        message = (
            f"⚠️ Only {success_count} out of {total} gateways were generated successfully."
        )

    return {"message": message}


@router.get("/gateways", response_model=GatewayMacListResponse)
def list_gateway_macs():
    """
    Retrieve list of gateway MAC addresses from the API.
    """
    macs = gateway_service.get_macs()

    if macs is None:
        return {"mac_addresses": [], "message": "❌ Failed to retrieve MAC addresses. API may be offline."}
    elif len(macs) == 0:
        return {"mac_addresses": [], "message": "⚠️ No MAC addresses found."}
    else:
        return {"mac_addresses": macs, "message": f"✅ {len(macs)} MAC addresses retrieved successfully."}
