import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import niquests
from fastapi import FastAPI
from fastapi.background import BackgroundTasks  # noqa: TC002
from fastapi.requests import Request  # noqa: TC002
from fastapi.responses import HTMLResponse  # noqa: TC002
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"
TEMPLATES_DIR = BASE_DIR.parent / "templates"
RANDOM_IMAGE_FILE = STATIC_DIR / "images" / "random.jpg"
CACHING_TTL_SECONDS = 10 * 60  # 10 minutes
BACKEND_HOST = os.getenv("BACKEND_HOST", "todo-backend")
BACKEND_PORT = os.getenv("BACKEND_PORT", "1245")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    if not RANDOM_IMAGE_FILE.exists():
        download_random_image()
    yield


app = FastAPI(title="Todo app", version="0.1.0", lifespan=lifespan)

app.mount(path="/static", app=StaticFiles(directory=Path(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/")
async def index(request: Request, background_tasks: BackgroundTasks) -> HTMLResponse:
    random_image_age_seconds = time.time() - RANDOM_IMAGE_FILE.stat().st_mtime

    if random_image_age_seconds >= CACHING_TTL_SECONDS:
        background_tasks.add_task(download_random_image)

    todos = await get_todos()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"todos": todos},
    )


def download_random_image() -> None:
    RANDOM_IMAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    response = niquests.get("https://picsum.photos/1200")
    response.raise_for_status()

    if not response.content:
        msg = "Failed to download random image"
        raise RuntimeError(msg)

    with (RANDOM_IMAGE_FILE).open("wb") as f:
        f.write(response.content)


async def get_todos() -> list[str]:
    response = niquests.get(url=f"http://{BACKEND_HOST}:{BACKEND_PORT}/todos")
    response.raise_for_status()

    if not isinstance(response.json(), list):
        raise RuntimeError("Failed to parse response from todo-backend")

    return response.json()
