from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncGenerator, TypedDict
from urllib.parse import urlencode

import httpx
from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api import router
from app.services.util import teardown_services


class State(TypedDict):
    http_client: httpx.AsyncClient


def get_lifespan():
    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[State]:
        try:
            logger.info("app start running")
            async with httpx.AsyncClient() as http_client:
                yield {"http_client": http_client}
        except Exception as exc:
            logger.exception(exc)
            raise
        finally:
            await teardown_services()
            await logger.complete()

    return lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        title="fastapi-ai-starter",
        lifespan=get_lifespan(),
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def exception_handler(_request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={"message": str(exc.detail)},
            )
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )

    @app.middleware("http")
    async def flatten_query_string_lists(request: Request, call_next):
        flattened: list[tuple[str, str]] = []
        for key, value in request.query_params.multi_items():
            flattened.extend((key, entry) for entry in value.split(","))

        request.scope["query_string"] = urlencode(flattened, doseq=True).encode("utf-8")

        return await call_next(request)

    app.include_router(router)

    add_pagination(app)

    return app
