from dataclasses import dataclass
from src.app.exceptions import IncorrectCredentialsException, ObjectNotFoundException
from src.app.usecase import IUseCase
from src.domain.entities.token import TokenPair, TokenPayload
from src.domain.entities.user import LoginUser
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.token_service import ITokenService
from src.domain.interfaces.uow import AbstractUOW
from src.domain.interfaces.user import IUserRepository


@dataclass
class LoginUserUseCase(IUseCase[LoginUser, TokenPair]):
    user_repostitory: IUserRepository
    password_manager: IPasswordManager
    token_service: ITokenService
    uow: AbstractUOW

    async def execute(self, input_dto: LoginUser) -> TokenPair:
        async with self.uow:
            user = await self.user_repostitory.get_user_by_email(email=input_dto.email)
            if user is None:
                raise ObjectNotFoundException(
                    message=f"User with email {input_dto.email} not found"
                )

        if not self.password_manager.verify_password(
            plain_password=input_dto.password, hashed_password=user.hashed_password
        ):
            raise IncorrectCredentialsException(message="Incorrect email or password")

        access_token = await self.token_service.create_access_token(
            token_payload=TokenPayload(user_id=user.id)
        )
        refresh_token = await self.token_service.create_refresh_token(
            token_payload=TokenPayload(user_id=user.id)
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
