import logging

from dishka import Provider, Scope, provide

from src.domain.interfaces.monitoring import IMonitoringRepository
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.token_service import ITokenService
from src.domain.interfaces.uow import AbstractUOW
from src.domain.interfaces.user import IUserRepository
from src.domain.usecases.login_user import LoginUserUseCase
from src.domain.usecases.monitoring import MonitoringUseCase
from src.domain.usecases.refresh_token import RefreshTokenUseCase
from src.domain.usecases.register_user import RegisterUserUseCase


log = logging.getLogger(__name__)


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def monitoring(
        self,
        monitoring_repository: IMonitoringRepository,
    ) -> MonitoringUseCase:
        return MonitoringUseCase(
            monitoring_repository=monitoring_repository,
        )

    @provide(scope=Scope.REQUEST)
    def register_user(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        token_service: ITokenService,
        uow: AbstractUOW,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repostitory=user_repository,
            password_manager=password_manager,
            token_service=token_service,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def login_user(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        token_service: ITokenService,
        uow: AbstractUOW,
    ) -> LoginUserUseCase:
        return LoginUserUseCase(
            user_repostitory=user_repository,
            password_manager=password_manager,
            token_service=token_service,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def refresh_token(
        self,
        token_service: ITokenService,
    ) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(token_service=token_service)
