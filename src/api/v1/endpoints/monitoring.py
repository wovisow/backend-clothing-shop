from fastapi import APIRouter


monitoring_router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)


@monitoring_router.get("/")
async def status(
    # monitoring_service: FromDishka[MonitoringService],
) -> dict:
    # return await monitoring_service.monitoring()
    return {"status": "alive"}
