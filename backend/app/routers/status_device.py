from fastapi import APIRouter, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from app.services import status_device_service

router = APIRouter()

@router.post("/loop")
def start_device_status_loop(
    background_tasks: BackgroundTasks,
    interval: int = Query(5, description="Interval in seconds between status sends")
):
    """
    Start continuous loop sending status from devices to the API.
    """
    try:
        background_tasks.add_task(status_device_service.start_device_status_loop, interval_seconds=interval)
        return JSONResponse(
            status_code=200,
            content={"message": f"Device status simulation started in background with interval of {interval} seconds."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error starting device status simulation: {str(e)}"}
        )


@router.post("/loop/stop")
def stop_device_status_loop():
    """
    Stop the background loop that sends device status.
    """
    try:
        status_device_service.stop_device_status_loop()
        return JSONResponse(
            status_code=200,
            content={"message": "🛑 Device status simulation loop has been stopped."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error stopping device status simulation: {str(e)}"}
        )

@router.get("/list")
def list_device_statuses():
    """
    Retrieve the list of device statuses from the API.
    """
    try:
        statuses = status_device_service.get_device_statuses()
        return JSONResponse(
            status_code=200,
            content={"device_statuses": statuses}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"❌ Error retrieving device statuses: {str(e)}"}
        )
