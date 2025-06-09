from fastapi import APIRouter, Query, BackgroundTasks
from fastapi.responses import JSONResponse

from app.services import gateway_status_service

router = APIRouter()


@router.post("/loop")
def start_status_loop(
    background_tasks: BackgroundTasks,
    interval: int = Query(5, description="Interval in seconds between each status sending")
):
    """
    Start continuous loop sending status from gateways to the API.
    """
    try:
        background_tasks.add_task(gateway_status_service.start_gateway_status_loop, interval_seconds=interval)
        return JSONResponse(
            status_code=200,
            content={"message": f"Gateway status simulation started in background with {interval}s interval."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error starting status simulation: {str(e)}"}
        )


@router.post("/stop")
def stop_status_loop():
    """
    Stop the background loop that sends gateway status.
    """
    try:
        gateway_status_service.stop_gateway_status_loop()
        return JSONResponse(
            status_code=200,
            content={"message": "🛑 Gateway status simulation loop has been stopped."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error stopping status loop: {str(e)}"})

@router.get("/list")
def list_gateway_statuses():
    """
    Retrieve the list of gateway statuses from the API.
    """
    try:
        statuses = gateway_status_service.get_gateway_statuses()
        return JSONResponse(
            status_code=200,
            content={"gateway_statuses": statuses}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error retrieving gateway statuses: {str(e)}"}
        )
