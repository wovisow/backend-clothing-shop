from dataclasses import dataclass
from src.app.usecase import IUseCase
from src.domain.entities.token import RefreshIn, TokenPair, TokenPayload
from src.domain.interfaces.token_service import ITokenService


@dataclass
class RefreshTokenUseCase(IUseCase[RefreshIn, TokenPair]):
    token_service: ITokenService

    async def execute(self, input_dto: RefreshIn) -> TokenPair:
        payload = await self.token_service.verify_refresh_token(
            token=input_dto.refresh_token
        )
        access_token = await self.token_service.create_access_token(
            token_payload=TokenPayload(user_id=payload.user_id)
        )
        refresh_token = await self.token_service.create_refresh_token(
            token_payload=TokenPayload(user_id=payload.user_id)
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
