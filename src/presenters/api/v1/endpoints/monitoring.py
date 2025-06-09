from dishka import FromDishka
from fastapi import APIRouter
from src.external.database.uow import SQLAlchemyUow
from src.presenters.api.v1.schemas.monitoring import MonitoringSchema
from src.domain.entities.base import BlankDTO
from src.domain.usecases.monitoring import MonitoringUseCase
from dishka.integrations.fastapi import DishkaRoute


monitoring_router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
    route_class=DishkaRoute,
)


@monitoring_router.get("/", response_model=MonitoringSchema)
async def status(
    monitoring: FromDishka[MonitoringUseCase], uow: FromDishka[SQLAlchemyUow]
) -> MonitoringSchema:
    async with uow:
        health = await monitoring.execute(input_dto=BlankDTO())
    return MonitoringSchema(health=health)
