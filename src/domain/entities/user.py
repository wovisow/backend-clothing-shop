from dataclasses import dataclass
from uuid import UUID

from src.external.database.tables import UserRole


@dataclass(frozen=True, kw_only=True, slots=True)
class UserRegister:
    name: str
    surname: str
    middlename: str
    email: str
    phone: str
    password: str


@dataclass(frozen=True, kw_only=True, slots=True)
class LoginUser:
    email: str
    password: str


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUser:
    name: str
    surname: str
    middlename: str | None
    email: str
    phone: str | None
    hashed_password: str
    role: UserRole


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    id: UUID
    name: str
    surname: str
    middlename: str | None
    email: str
    phone: str | None
    hashed_password: str
    role: UserRole
