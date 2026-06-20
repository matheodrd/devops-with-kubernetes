FROM python:3.14-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -m -s /sbin/nologin appuser

RUN chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser . .

CMD ["python", "main.py"]
