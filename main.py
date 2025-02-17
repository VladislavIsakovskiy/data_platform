import os

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from data_platform.logger_config import logger

from data_platform.config import settings
from data_platform.routers import router as de_router
from data_platform.database.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create_app() -> FastAPI:
    dp_app = FastAPI(
        title="Data platform service",
        description="API for Data platform service",
        lifespan=lifespan,
    )

    @dp_app.get("/healthcheck", include_in_schema=False)
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return dp_app


app = create_app()

app.include_router(de_router, prefix="/v1")


@app.middleware("http")
async def request_log(request: Request, call_next):
    """
    Global exception handler for catching non API errors.
    ALso catch, sort and write uvicorn output and critical errors to log
    :param request: Request
    :param call_next: call_next
    :return: JSONResponse
    """
    try:
        response: Response = await call_next(request)
        if response.status_code < 400:
            logger.info(f"{request.method} {request.url} Status code: {response.status_code}")
        else:
            logger.warning(f"{request.method} {request.url} Status code: {response.status_code}")
        return response
    except Exception as exc:  # noqa
        logger.exception(str(exc))
        return ORJSONResponse(
            status_code=500,
            content={"message": "Something went wrong!"},
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        log_config=f"{os.getcwd()}/../uvicorn_disable_logging.json",
        reload=True,
    )