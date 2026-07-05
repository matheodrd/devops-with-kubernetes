from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from anyio import Path
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

OUTPUT_DIR = Path("/usr/share/data/ping-pong")
OUTPUT_FILE = OUTPUT_DIR / "counter"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if await OUTPUT_FILE.exists():
        try:
            content = await OUTPUT_FILE.read_text()
            app.state.counter = int(content.strip())
        except ValueError, TypeError:
            app.state.counter = 0
    else:
        app.state.counter = 0
        await OUTPUT_FILE.write_text("0")
    yield


app = FastAPI(title="Ping Pong", lifespan=lifespan)


@app.get("/pingpong", response_class=PlainTextResponse)
async def ping_pong(request: Request) -> str:
    request.app.state.counter += 1
    current_count = request.app.state.counter

    await OUTPUT_FILE.write_text(str(current_count))

    return f"pong {current_count}"
