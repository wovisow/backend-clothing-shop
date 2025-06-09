from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from enum import Enum
import logging
from typing import Any
import sqlalchemy.dialects.postgresql as pg


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

log = logging.getLogger(__name__)


@asynccontextmanager
async def create_engine(dsn: str, debug: bool) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        url=dsn,
        echo=debug,
        pool_size=15,
        max_overflow=10,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


def create_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def make_pg_enum(enum_cls: type[Enum], **kwargs: Any) -> pg.ENUM:
    return pg.ENUM(
        enum_cls,
        values_callable=_choices,
        **kwargs,
    )


def _choices(enum_cls: type[Enum]) -> tuple[str, ...]:
    return tuple(map(str, enum_cls))
