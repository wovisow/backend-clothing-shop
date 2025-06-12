import logging

from dishka import Provider, Scope, provide

from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.token_service import ITokenService
from src.external.jwt_token_service import JWTTokenService
from src.external.password_manager import PasswordManager


log = logging.getLogger(__name__)


class ExternalProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def jwt_token_service(
        self,
    ) -> ITokenService:
        return JWTTokenService(
            secret_key="terces",
            algorithm="HS256",
            access_token_expires_seconds=3600,
            refresh_token_expires_seconds=3600,
        )

    @provide(scope=Scope.REQUEST)
    def password_manager(
        self,
    ) -> IPasswordManager:
        return PasswordManager()
