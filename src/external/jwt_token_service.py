import time
from collections.abc import Mapping
from enum import StrEnum, unique
from typing import Any
from uuid import UUID

from jose import JWTError, jwt

from src.domain.entities.token import TokenPayload
from src.domain.interfaces.token_service import ITokenService


@unique
class Scopes(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTTokenService(ITokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expires_seconds: int,
        refresh_token_expires_seconds: int,
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_token_expires_seconds = access_token_expires_seconds
        self.__refresh_token_expires_seconds = refresh_token_expires_seconds

    async def create_access_token(self, *, token_payload: TokenPayload) -> str:
        payload = {
            "sub": str(token_payload.user_id),
            "scope": Scopes.ACCESS,
        }
        return self._encode(payload, self.__access_token_expires_seconds)

    async def create_refresh_token(self, *, token_payload: TokenPayload) -> str:
        payload = {
            "sub": str(token_payload.user_id),
            "scope": Scopes.REFRESH,
        }
        return self._encode(payload, self.__refresh_token_expires_seconds)

    async def verify_access_token(self, *, token: str) -> TokenPayload:
        payload = self._decode(token)
        if payload.get("scope") != Scopes.ACCESS:
            raise JWTError("Expected access token")
        return TokenPayload(
            user_id=UUID(payload["sub"]),
        )

    async def verify_refresh_token(self, *, token: str) -> TokenPayload:
        payload = self._decode(token)
        if payload.get("scope") != Scopes.REFRESH:
            raise JWTError("Expected refresh token")
        return TokenPayload(
            user_id=UUID(payload["sub"]),
        )

    async def refresh_access_token(self, *, refresh_token: str) -> str:
        token_payload = await self.verify_refresh_token(token=refresh_token)
        return await self.create_access_token(token_payload=token_payload)

    def _encode(self, payload: Mapping[str, Any], exp: int) -> str:
        issued = int(time.time())
        to_encode = {**payload, "iat": issued, "exp": issued + exp}
        return jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)

    def _decode(self, token: str) -> Mapping[str, Any]:
        try:
            return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        except JWTError:
            return {}
