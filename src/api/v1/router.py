from fastapi import APIRouter
from src.api.v1.endpoints.monitoring import monitoring_router


router = APIRouter(prefix="/v1")
router.include_router(monitoring_router)
