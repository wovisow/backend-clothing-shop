from src.app.config.base import AppBaseSettings, Environment


class AppProdSettings(AppBaseSettings):
    description: str | None = "Production Environment."
    environment: Environment = Environment.PROD
