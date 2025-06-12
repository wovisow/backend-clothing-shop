from collections.abc import AsyncIterator
from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide

from src.domain.interfaces.monitoring import IMonitoringRepository
from src.domain.interfaces.uow import AbstractUOW
from src.domain.interfaces.user import IUserRepository
from src.external.database.repositories.monitoring import PGMonitoringRepository
from src.external.database.repositories.user import PGUserRepository
from src.external.database.uow import SQLAlchemyUow
from src.external.database.utils import create_engine, create_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class DBProvider(Provider):
    def __init__(
        self,
        dsn: str,
        debug: bool,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.dsn = dsn
        self.debug = debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(dsn=self.dsn, debug=self.debug) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[SQLAlchemyUow, AbstractUOW]:
        return SQLAlchemyUow(session=session_factory())

    @provide(scope=Scope.REQUEST)
    async def db_monitoring_repository(
        self,
        uow: SQLAlchemyUow,
    ) -> IMonitoringRepository:
        return PGMonitoringRepository(session=uow.session)

    @provide(scope=Scope.REQUEST)
    async def db_user_repository(
        self,
        uow: SQLAlchemyUow,
    ) -> IUserRepository:
        return PGUserRepository(session=uow.session)
