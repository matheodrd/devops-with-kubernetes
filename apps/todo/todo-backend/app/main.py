from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Annotated

from fastapi import FastAPI, Form
from fastapi.requests import Request  # noqa: TC002
from fastapi.responses import RedirectResponse  # noqa: TC002

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    app.state.todos = []
    yield


app = FastAPI(title="Todo backend", version="0.1.0", lifespan=lifespan)


@app.get("/todos")
async def get_todos(request: Request) -> list[str]:
    return request.app.state.todos


@app.post("/todos")
async def add_todo(
    request: Request, todo: Annotated[str, Form(...)]
) -> RedirectResponse:
    if todo.strip():
        request.app.state.todos.append(todo.strip())
    return RedirectResponse(url="/", status_code=303)
