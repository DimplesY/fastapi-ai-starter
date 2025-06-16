from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.api import router
from contextlib import asynccontextmanager

from app.services.util import initialize_services


def get_lifespan():
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        try:
            await initialize_services()
            yield
        except Exception as exc:
            raise RuntimeError(f"Unexpected error: {exc}") from exc

    return lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        title="fastapi celery starter",
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

    app.include_router(router)

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

    return app
