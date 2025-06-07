from pydantic_settings import BaseSettings


from enum import StrEnum


class Environment(StrEnum):
    PROD = "PROD"
    DEVELOP = "DEV"
    # STAGE = "STAGE"


class AppBaseSettings(BaseSettings):
    title: str = "Application"
    version: str = "0.1.0"
    timezone: str = "UTC"
    description: str = ""
    debug: bool = False
