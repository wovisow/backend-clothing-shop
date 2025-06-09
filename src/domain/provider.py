import logging

from dishka import Provider, Scope, provide

from src.domain.interfaces.monitoring import IMonitoringRepository
from src.domain.usecases.monitoring import MonitoringUseCase


log = logging.getLogger(__name__)


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def monitoring(
        self,
        monitoring_repository: IMonitoringRepository,
    ) -> MonitoringUseCase:
        return MonitoringUseCase(monitoring_repository=monitoring_repository)
