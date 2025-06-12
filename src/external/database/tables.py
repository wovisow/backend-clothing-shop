from datetime import datetime
import enum
from sqlalchemy import Boolean, ForeignKey, Integer, String
from src.external.database.base import BaseTable, IdentifiableMixin, TimestampedMixin
from sqlalchemy.orm import Mapped, mapped_column

from src.external.database.utils import make_pg_enum
from sqlalchemy.orm import relationship


class ProductSize(enum.Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class ProductColor(enum.Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    WHITE = "white"
    GREEN = "green"


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    TAILOR = "tailor"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PREPARING = "preparing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ShipmentStatus(enum.Enum):
    PREPARING = "preparing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ShippingCompany(enum.Enum):
    CDEK = "cdek"
    EVO = "evo"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class PaymentMethod(enum.Enum):
    CARD = "card"
    PAYPAL = "paypal"
    SBP = "sbp"


class UserTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    surname: Mapped[str] = mapped_column(String(64), nullable=False)
    middlename: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(32), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        make_pg_enum(UserRole), default=UserRole.CUSTOMER
    )


class ProductTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    size: Mapped[ProductSize] = mapped_column(make_pg_enum(ProductSize))
    color: Mapped[ProductColor] = mapped_column(make_pg_enum(ProductColor))
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    category: Mapped["CategoryTable"] = relationship(back_populates="products")


class CategoryTable(BaseTable, IdentifiableMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    products: Mapped[list["ProductTable"]] = relationship(
        back_populates="category",
    )


class CartItemTable(BaseTable, IdentifiableMixin):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart: Mapped["CartTable"] = relationship(back_populates="items")
    product: Mapped["ProductTable"] = relationship()


class CartTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserTable"] = relationship()
    items: Mapped[list["CartItemTable"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
    )


class OrderItemTable(BaseTable, IdentifiableMixin):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["OrderTable"] = relationship(back_populates="items")
    product: Mapped["ProductTable"] = relationship()


class OrderTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        make_pg_enum(OrderStatus),
        default=OrderStatus.PENDING,
    )
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    shipping_address: Mapped[str] = mapped_column(String(256), nullable=False)

    items: Mapped[list["OrderItemTable"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
    user: Mapped["UserTable"] = relationship()


class ShipmentTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "shipments"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    status: Mapped[ShipmentStatus] = mapped_column(
        make_pg_enum(ShipmentStatus),
        default=ShipmentStatus.PREPARING,
    )
    shipped_at: Mapped[datetime | None] = mapped_column(nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(nullable=True)
    tracking_number: Mapped[str | None] = mapped_column(String(128), nullable=True)
    shipping_company: Mapped[ShippingCompany] = mapped_column(
        make_pg_enum(ShippingCompany),
        default=ShippingCompany.CDEK,
    )

    order: Mapped["OrderTable"] = relationship()


class PaymentTable(BaseTable, IdentifiableMixin, TimestampedMixin):
    __tablename__ = "payments"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        make_pg_enum(PaymentStatus),
        default=PaymentStatus.PENDING,
    )
    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)
    method: Mapped[PaymentMethod] = mapped_column(make_pg_enum(PaymentMethod))

    order: Mapped["OrderTable"] = relationship()
