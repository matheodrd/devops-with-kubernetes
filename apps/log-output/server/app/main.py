from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

OUTPUT_DIR = Path("./files/")
OUTPUT_FILE = Path(OUTPUT_DIR / "output")

app = FastAPI(title="Log output")


def read_random_string() -> str:
    with OUTPUT_FILE.open("r") as f:
        return f.read()


@app.get("/", response_class=PlainTextResponse)
async def get_status(
    random_string: Annotated[str, Depends(read_random_string)],
) -> str:
    return random_string
