from src.application.config.base import AppBaseSettings, Environment


class AppDevSettings(AppBaseSettings):
    description: str | None = "Development Environment."
    debug: bool = True
    environment: Environment = Environment.DEVELOP
