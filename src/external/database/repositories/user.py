import logging
from typing import NoReturn

from src.app.exceptions import RepositoryException
from src.domain.entities.user import CreateUser, User
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, IntegrityError


from src.domain.interfaces.user import IUserRepository
from src.external.database.tables import UserTable


log = logging.getLogger(__name__)


class PGUserRepository(IUserRepository):
    __session: AsyncSession

    def __init__(self, *, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, input_dto: CreateUser) -> User:
        stmt = (
            insert(UserTable)
            .values(
                name=input_dto.name,
                surname=input_dto.surname,
                middlename=input_dto.middlename,
                email=input_dto.email,
                phone=input_dto.phone,
                role=input_dto.role,
                hashed_password=input_dto.hashed_password,
            )
            .returning(UserTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self._raise_exception(e)

        return User(
            id=result.id,
            name=result.name,
            surname=result.surname,
            middlename=result.middlename,
            email=result.email,
            phone=result.phone,
            hashed_password=result.hashed_password,
            role=result.role,
        )

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(UserTable).where(UserTable.email == email)
        result = await self.__session.scalar(stmt)
        if result is None:
            return None

        return User(
            id=result.id,
            name=result.name,
            surname=result.surname,
            middlename=result.middlename,
            email=result.email,
            phone=result.phone,
            hashed_password=result.hashed_password,
            role=result.role,
        )

    def _raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "uq_users_email":
                raise RepositoryException(
                    "Cannot create User: User with email already exist"
                )

        log.warning("DB error: %s", e)
        raise RepositoryException(self.__class__.__name__)
