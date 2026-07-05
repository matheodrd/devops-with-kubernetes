FROM python:3.14.6-slim-trixie@sha256:44dd04494ee8f3b538294360e7c4b3acb87c8268e4d0a4828a6500b1eff50061

RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser --no-create-home -s /sbin/nologin appuser

WORKDIR /app
RUN chown appuser:appuser /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --chown=appuser:appuser main.py ./

USER appuser

CMD ["python", "main.py"]
