import os
from pathlib import Path
from typing import Annotated

import niquests
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

LOG_OUTPUT_FILE = Path("./files/output")
PING_PONG_API_HOST = os.getenv("PING_PONG_API_HOST", "ping-pong")
PING_PONG_API_PORT = os.getenv("PING_PONG_API_PORT", "1236")

app = FastAPI(title="Log output")


def read_random_string() -> str:
    try:
        with LOG_OUTPUT_FILE.open("r") as f:
            return f.read()
    except FileNotFoundError:
        return "No string generated yet"


async def get_pings() -> int:
    response = await niquests.aget(
        f"http://{PING_PONG_API_HOST}:{PING_PONG_API_PORT}/pings"
    )
    response.raise_for_status()

    if not response.content:
        return 0
    return response.json()["data"]


@app.get("/", response_class=PlainTextResponse)
async def get_status(
    random_string: Annotated[str, Depends(read_random_string)],
    pings: Annotated[int, Depends(get_pings)],
) -> str:
    return f"{random_string}.\nPing / Pongs: {pings}"
