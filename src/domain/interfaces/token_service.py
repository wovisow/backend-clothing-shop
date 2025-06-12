from abc import ABC, abstractmethod

from src.domain.entities.token import TokenPayload


class ITokenService(ABC):
    @abstractmethod
    async def create_access_token(self, *, token_payload: TokenPayload) -> str: ...

    @abstractmethod
    async def create_refresh_token(self, *, token_payload: TokenPayload) -> str: ...

    @abstractmethod
    async def verify_access_token(self, *, token: str) -> TokenPayload: ...

    @abstractmethod
    async def verify_refresh_token(self, *, token: str) -> TokenPayload: ...

    @abstractmethod
    async def refresh_access_token(self, *, refresh_token: str) -> str: ...
