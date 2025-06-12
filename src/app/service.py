from contextlib import asynccontextmanager
from dataclasses import dataclass
import logging
from typing import AsyncIterator
from dishka.integrations.fastapi import setup_dishka

from dishka import make_async_container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.external.provider import ExternalProvider
from src.presenters.api.router import api_router
from src.app.config import AppBaseSettings
from src.domain.provider import DomainProvider
from src.external.database.provider import DBProvider


log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    log.info("App startup")
    yield
    log.info("App shutdown")


@dataclass(frozen=True, slots=True, kw_only=True)
class RestService:
    config: AppBaseSettings

    def create_application(self) -> FastAPI:
        app = FastAPI(
            debug=self.config.debug,
            title=self.config.title,
            description=self.config.description,
            version=self.config.version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
            lifespan=lifespan,
        )
        self.set_middlewares(app=app)
        self.set_routes(app=app)
        self.set_exceptions(app=app)
        self.set_dependencies(app=app)

        log.info("Rest service configured")
        return app

    def set_middlewares(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def set_routes(self, app: FastAPI) -> None:
        app.include_router(api_router)

    def set_exceptions(self, app: FastAPI) -> None:
        ...
        # for exception, handler in EXCEPTION_HANDLERS:
        # app.add_exception_handler(exception, handler)

    def set_dependencies(self, app: FastAPI) -> None:
        container = make_async_container(
            DomainProvider(),
            DBProvider(
                dsn=self.config.db.dsn_url,
                debug=self.config.debug,
            ),
            ExternalProvider(),
            skip_validation=True,
        )
        setup_dishka(container=container, app=app)
