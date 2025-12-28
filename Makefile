CONTAINER_ENGINE := $(shell if command -v podman >/dev/null 2>&1; then echo podman; else echo docker; fi)
LAST_TAG := $(shell git describe --tags --abbrev=0 --match "v*.*.*" 2>/dev/null || echo "v0.0.0")
VERSION := $(patsubst v%,%,$(LAST_TAG))
BUILD_COMMIT := $(shell git rev-parse --short HEAD)

.PHONY: init test dev format lint build run container-build container-run container-stop container-logs container-destroy help

init:
	@ln -sf $(CURDIR)/.hooks/pre-commit.sh .git/hooks/pre-commit
	@uv sync

update:
	@uv lock --upgrade
	@uv sync

test:
	@uv run pytest --verbose --junit-xml=tests/coverage.xml

dev:
	@uv run alembic upgrade head
	@uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

format:
	@uv run ruff format --force-exclude -- app

lint:
	@uv run ruff check --quiet --force-exclude -- app
	@uv run mypy --pretty -- app

build:
	@SETUPTOOLS_SCM_PRETEND_VERSION=$(VERSION)+$(BUILD_COMMIT) uv run python -m build --outdir dist

run:
	@uv run alembic upgrade head
	@uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --no-access-log

container-build:
	@REVISION=$(BUILD_COMMIT) $(CONTAINER_ENGINE) compose build

container-run:
	@REVISION=$(BUILD_COMMIT) $(CONTAINER_ENGINE) compose up --detach

container-stop:
	@REVISION=$(BUILD_COMMIT) $(CONTAINER_ENGINE) compose down

container-logs:
	@REVISION=$(BUILD_COMMIT) $(CONTAINER_ENGINE) compose logs --follow

container-destroy:
	@REVISION=$(BUILD_COMMIT) $(CONTAINER_ENGINE) compose down --volumes --rmi local

help:
	@echo "Available targets:"
	@echo "  init              - Set up py venv and install requirements"
	@echo "  test              - Run tests"
	@echo "  dev               - Start app in development mode"
	@echo "  format            - Run format on all python files"
	@echo "  lint              - Run lint on all python files"
	@echo "  build             - Build the app package"
	@echo "  run               - Run the app"
	@echo "  container-build   - Build app in containers and create container image"
	@echo "  container-run     - Run app container"
	@echo "  container-stop    - Stop app container"
	@echo "  container-logs    - Show app container logs"
	@echo "  container-destroy - Stop and delete app container, networks, volumes, and images"
	@echo "  help              - Show this help message"
