from datetime import UTC, datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, MetaData, text
from sqlalchemy import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    declared_attr,
    mapped_column,
)
from sqlalchemy.ext.asyncio import AsyncAttrs


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseTable(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


@declarative_mixin
class TimestampedMixin:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
            server_onupdate=text("TIMEZONE('utc', now())"),
            onupdate=now_with_tz,
        )

    @declared_attr
    def deleted_at(cls) -> Mapped[datetime | None]:
        return mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )


@declarative_mixin
class IdentifiableMixin:
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            PGUUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        )


def now_with_tz() -> datetime:
    return datetime.now(tz=UTC)
