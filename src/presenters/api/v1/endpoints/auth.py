from http import HTTPStatus
from dishka import FromDishka
from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from src.domain.entities.token import RefreshIn
from src.domain.entities.user import LoginUser, UserRegister
from src.domain.usecases.login_user import LoginUserUseCase
from src.domain.usecases.refresh_token import RefreshTokenUseCase
from src.domain.usecases.register_user import RegisterUserUseCase
from src.presenters.api.v1.schemas.auth import (
    LoginUserSchema,
    RefreshInSchema,
    TokenPairSchema,
    UserRegisterSchema,
)


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@auth_router.post(
    "/register",
    response_model=TokenPairSchema,
    status_code=HTTPStatus.CREATED,
)
async def register(
    register_user: FromDishka[RegisterUserUseCase],
    payload: UserRegisterSchema,
) -> TokenPairSchema:
    token_pair = await register_user.execute(
        input_dto=UserRegister(
            name=payload.name,
            surname=payload.surname,
            middlename=payload.middlename,
            email=payload.email,
            phone=payload.phone,
            password=payload.password,
        ),
    )
    return TokenPairSchema.model_validate(token_pair)


@auth_router.post(
    "/login",
    response_model=TokenPairSchema,
    status_code=HTTPStatus.OK,
)
async def login(
    payload: LoginUserSchema,
    login_user: FromDishka[LoginUserUseCase],
) -> TokenPairSchema:
    token_pair = await login_user.execute(
        input_dto=LoginUser(
            email=payload.email,
            password=payload.password,
        ),
    )
    return TokenPairSchema.model_validate(token_pair)


@auth_router.post(
    "/refresh",
    response_model=TokenPairSchema,
    status_code=HTTPStatus.OK,
)
async def refresh_tokens(
    payload: RefreshInSchema,
    refresh_token: FromDishka[RefreshTokenUseCase],
) -> TokenPairSchema:
    token_pair = await refresh_token.execute(
        input_dto=RefreshIn(
            refresh_token=payload.refresh_token,
        ),
    )
    return TokenPairSchema.model_validate(token_pair)
