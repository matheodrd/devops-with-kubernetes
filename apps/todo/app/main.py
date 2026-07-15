import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import niquests
from fastapi import FastAPI
from fastapi.background import BackgroundTasks  # noqa: TC002
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"
RANDOM_IMAGE_FILE = STATIC_DIR / "images" / "random.jpg"
CACHING_TTL_SECONDS = 10 * 60  # 10 minutes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    if not RANDOM_IMAGE_FILE.exists():
        download_random_image()
    yield


app = FastAPI(title="Todo app", version="0.1.0", lifespan=lifespan)

app.mount(path="/static", app=StaticFiles(directory=Path(STATIC_DIR)), name="static")


@app.get("/")
async def index(background_tasks: BackgroundTasks) -> HTMLResponse:
    random_image_age_seconds = time.time() - RANDOM_IMAGE_FILE.stat().st_mtime

    if random_image_age_seconds >= CACHING_TTL_SECONDS:
        background_tasks.add_task(download_random_image)

    html_content = """
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Todo app</title>
            <link rel="stylesheet" href="/static/css/vendor/simple.min.css" />
        </head>
        <body>
            <main>
                <h1 style="text-align: center; margin-top: 0;">Todo App</h1>
                <figure style="text-align: center; margin: auto;">
                    <img src="/static/images/random.jpg" alt="random image" style="max-width: 25%; min-width: 150px; margin: auto;">
                    <figcaption>DevOps with Kubernetes</figcaption>
                </figure>

                <div style="text-align: center; margin: auto;">
                    <input type="text" name="new-todo" placeholder="Enter a new todo (max 140 characters)" maxlength="140" />
                    <button type="submit">Send</button>
                </div>
            </main>
        </body>
    </html>
    """  # noqa: E501
    return HTMLResponse(content=html_content, status_code=200)


def download_random_image() -> None:
    RANDOM_IMAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    response = niquests.get("https://picsum.photos/1200")
    response.raise_for_status()

    if not response.content:
        msg = "Failed to download random image"
        raise RuntimeError(msg)

    with (RANDOM_IMAGE_FILE).open("wb") as f:
        f.write(response.content)
