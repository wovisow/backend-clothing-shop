from pydantic_settings import BaseSettings, SettingsConfigDict


from enum import StrEnum


class Environment(StrEnum):
    PROD = "PROD"
    DEVELOP = "DEV"
    # STAGE = "STAGE"


class DBSettings(BaseSettings):
    user: str = "user"
    password: str = "user"
    host: str = "localhost"
    port: int = 5432
    name: str = "shop"
    echo: bool = False

    @property
    def dsn_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_prefix="DB_")


class AppBaseSettings(BaseSettings):
    title: str = "Application"
    version: str = "0.1.0"
    timezone: str = "UTC"
    description: str = ""
    debug: bool = False

    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(env_prefix="APP_")
