## BUILDER ##
FROM ghcr.io/astral-sh/uv:0.11.23-python3.14-trixie-slim@sha256:ac6a11294d8d964632c4000cba0f81a508befd7d4cdaf6022cde9e4655bc641e AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

## RUNTIME ##
FROM python:3.14.6-slim-trixie@sha256:44dd04494ee8f3b538294360e7c4b3acb87c8268e4d0a4828a6500b1eff50061 AS runtime

ENV PORT=8000

RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser --no-create-home -s /sbin/nologin appuser

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser static/ ./static
COPY --chown=appuser:appuser templates/ ./templates

USER appuser

EXPOSE $PORT

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1"]
