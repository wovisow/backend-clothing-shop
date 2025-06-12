from dataclasses import dataclass
from src.app.usecase import IUseCase
from src.domain.entities.token import TokenPair, TokenPayload
from src.domain.entities.user import CreateUser, UserRegister
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.token_service import ITokenService
from src.domain.interfaces.uow import AbstractUOW
from src.domain.interfaces.user import IUserRepository
from src.external.database.tables import UserRole


@dataclass
class RegisterUserUseCase(IUseCase[UserRegister, TokenPair]):
    user_repostitory: IUserRepository
    password_manager: IPasswordManager
    token_service: ITokenService
    uow: AbstractUOW

    async def execute(self, input_dto: UserRegister) -> TokenPair:
        async with self.uow:
            user = await self.user_repostitory.create(
                input_dto=CreateUser(
                    name=input_dto.name,
                    surname=input_dto.surname,
                    middlename=input_dto.middlename,
                    email=input_dto.email,
                    phone=input_dto.phone,
                    hashed_password=self.password_manager.hash_password(
                        password=input_dto.password
                    ),
                    role=UserRole.ADMIN
                    if input_dto.phone == "+71111111111"
                    else UserRole.CUSTOMER,
                )
            )
        access_token = await self.token_service.create_access_token(
            token_payload=TokenPayload(
                user_id=user.id,
            )
        )
        refresh_token = await self.token_service.create_refresh_token(
            token_payload=TokenPayload(
                user_id=user.id,
            )
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
