FROM docker.io/library/python:3.13-slim
ARG REVISION
LABEL org.opencontainers.image.title="FastAPI Template"
LABEL org.opencontainers.image.description="FastAPI Template"
LABEL org.opencontainers.image.source="https://github.com/zbhavyai/fastapi-template"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Bhavyai Gupta <https://zbhavyai.github.io>"
LABEL org.opencontainers.image.version="${REVISION}"
WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/opt/app
RUN apt-get update && apt-get install -y --no-install-recommends curl
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir --requirement requirements.txt
COPY pyproject.toml pyproject.toml
COPY app app
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 CMD curl --fail --silent --show-error http://localhost:8080/api/ping || exit 1
EXPOSE 8080
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]
