from abc import abstractmethod
from typing import Protocol

from src.domain.entities.user import CreateUser, User


class IUserRepository(Protocol):
    @abstractmethod
    async def create(self, input_dto: CreateUser) -> User: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None: ...
