from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.counter = 0
    yield


app = FastAPI(title="Ping Pong", lifespan=lifespan)


def increment_counter(request: Request) -> int:
    request.app.state.counter += 1
    return request.app.state.counter


@app.get("/pingpong", response_class=PlainTextResponse)
async def ping_pong(
    counter: Annotated[int, Depends(increment_counter)],
) -> str:
    return f"pong {counter}"
