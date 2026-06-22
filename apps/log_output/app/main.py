import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Request

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


async def log_loop(app: FastAPI) -> None:
    while True:
        logger.info(f"{datetime.now(UTC)}: {app.state.random_string}")
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.random_string = str(uuid4())
    asyncio.create_task(log_loop(app))
    yield


app = FastAPI(title="Log output", lifespan=lifespan)

logger = logging.getLogger("uvicorn.error")


def get_random_string(request: Request) -> str:
    return request.app.state.random_string


@app.get("/status")
async def get_status(
    random_string: Annotated[str, Depends(get_random_string)],
) -> dict[str, str]:
    return {
        "timestamp": str(datetime.now(UTC)),
        "random_string": random_string,
    }
