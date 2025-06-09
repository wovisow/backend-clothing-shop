from dataclasses import dataclass
from src.app.usecase import IUseCase
from src.domain.entities.base import BlankDTO
from src.domain.interfaces.monitoring import IMonitoringRepository


@dataclass
class MonitoringUseCase(IUseCase[BlankDTO, bool]):
    monitoring_repository: IMonitoringRepository

    async def execute(self, *, input_dto: BlankDTO) -> bool:
        return await self.monitoring_repository.check_connection()
