# build stage
FROM docker.io/library/python:3.14-slim as build
ARG REVISION
WORKDIR /opt/app
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${REVISION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/app \
    PATH="/opt/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/
COPY pyproject.toml uv.lock README.md LICENSE alembic.ini ./
COPY app ./app
COPY migrations ./migrations
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-group dev

# runtime stage
FROM docker.io/library/python:3.14-slim
ARG REVISION
LABEL org.opencontainers.image.title="FastAPI Template"
LABEL org.opencontainers.image.description="FastAPI Template"
LABEL org.opencontainers.image.source="https://github.com/zbhavyai/fastapi-template"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Bhavyai Gupta <https://zbhavyai.github.io>"
LABEL org.opencontainers.image.version="${REVISION}"
WORKDIR /opt/app
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${REVISION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/app \
    PATH="/opt/app/.venv/bin:$PATH"
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/app /opt/app
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 CMD curl --fail --silent --show-error http://localhost:8080/api/ping || exit 1
EXPOSE 8080
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
