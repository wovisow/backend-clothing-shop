from contextlib import asynccontextmanager
from dataclasses import dataclass
import logging
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.application.config import AppBaseSettings


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

    def set_dependencies(self, app: FastAPI) -> None: ...
