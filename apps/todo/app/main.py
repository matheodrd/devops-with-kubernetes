from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

app = FastAPI(title="Todo app", version="0.1.0")

app.mount(path="/static", app=StaticFiles(directory=Path(STATIC_DIR)), name="static")


@app.get("/")
async def index() -> HTMLResponse:
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
            <header>
                <h1>Todo App</h1>
            </header>
            <main>
                <p>DevOps with Kubernetes</p>
            </main>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
