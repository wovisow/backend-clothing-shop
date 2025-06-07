from functools import lru_cache
from decouple import config

from src.application.config.base import AppBaseSettings, Environment
from src.application.config.development import AppDevSettings
from src.application.config.production import AppProdSettings


@lru_cache
def app_settings_factory() -> AppBaseSettings:
    environment = config("ENVIRONMENT", default="DEV", cast=str)

    match environment:
        case Environment.PROD.value:
            return AppProdSettings()
        case _:
            return AppDevSettings()


settings: AppBaseSettings = app_settings_factory()
