from sqlalchemy import String
from src.external.database.base import BaseTable, IdentifiableMixin, TimestampedMixin
from sqlalchemy.orm import Mapped, mapped_column


class ProductTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(128), nullable=False)
