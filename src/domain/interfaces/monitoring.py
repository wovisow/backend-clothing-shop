from abc import abstractmethod
from typing import Protocol


class IMonitoringRepository(Protocol):
    @abstractmethod
    async def check_connection(self) -> bool: ...
