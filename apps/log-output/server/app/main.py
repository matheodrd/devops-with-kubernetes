from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

LOG_OUTPUT_FILE = Path("./files/output")
PING_PONG_COUNTER_FILE = Path("/usr/share/data/ping-pong/counter")

app = FastAPI(title="Log output")


def read_random_string() -> str:
    try:
        with LOG_OUTPUT_FILE.open("r") as f:
            return f.read()
    except FileNotFoundError:
        return "No string generated yet"


def read_ping_pong_count() -> str:
    if not PING_PONG_COUNTER_FILE.exists():
        return "0"
    try:
        with PING_PONG_COUNTER_FILE.open("r") as f:
            return f.read()
    except Exception:
        return "0"


@app.get("/", response_class=PlainTextResponse)
async def get_status(
    random_string: Annotated[str, Depends(read_random_string)],
    ping_pong_count: Annotated[str, Depends(read_ping_pong_count)],
) -> str:
    return f"{random_string}.\nPing / Pongs: {ping_pong_count}"
