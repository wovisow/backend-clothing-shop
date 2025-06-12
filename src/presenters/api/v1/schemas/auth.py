from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterSchema(BaseModel):
    name: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    middlename: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=12)
    password: str = Field(min_length=5)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshInSchema(BaseModel):
    refresh_token: str


class TokenPairSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
