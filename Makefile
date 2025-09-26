CONTAINER_ENGINE := $(shell if command -v podman >/dev/null 2>&1; then echo podman; else echo docker; fi)
REVISION := $(shell git rev-parse --short HEAD)
VENV_DIR := .venv/PY-VENV
REQUIREMENTS_FILE := requirements.txt

.PHONY: prep dev format lint run container-build container-run container-stop container-logs container-destroy help

define CHECK_DEPENDENCY
	@for cmd in $(1); do \
		if ! command -v $$cmd &>/dev/null; then \
			echo "Couldn't find $$cmd!"; \
			exit 1; \
		fi; \
	done
endef

.deps-container:
	$(call CHECK_DEPENDENCY, $(CONTAINER_ENGINE))

prep: $(REQUIREMENTS_FILE)
	@ln -sf $(CURDIR)/.hooks/pre-commit.sh .git/hooks/pre-commit
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
	fi
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)

dev:
	@. $(VENV_DIR)/bin/activate && fastapi dev app/main.py --host 0.0.0.0 --port 8080

format:
	@. $(VENV_DIR)/bin/activate && \
	ruff format --force-exclude -- app

lint:
	@. $(VENV_DIR)/bin/activate && \
	ruff check --force-exclude -- app && \
	mypy --pretty -- app

run:
	@. $(VENV_DIR)/bin/activate && fastapi run app/main.py --host 0.0.0.0 --port 8080

container-build: .deps-container
	@REVISION=$(REVISION) $(CONTAINER_ENGINE) compose build

container-run: .deps-container
	@REVISION=$(REVISION) $(CONTAINER_ENGINE) compose up --detach

container-stop: .deps-container
	@REVISION=$(REVISION) $(CONTAINER_ENGINE) compose down

container-logs: .deps-container
	@REVISION=$(REVISION) $(CONTAINER_ENGINE) compose logs --follow

container-destroy: .deps-container
	@REVISION=$(REVISION) $(CONTAINER_ENGINE) compose down --volumes --rmi local

help:
	@echo "Available targets:"
	@echo "  prep              - Set up py venv and install requirements"
	@echo "  dev               - Start app in development mode"
	@echo "  lint              - Run lint on all python files"
	@echo "  format            - Run format on all python files"
	@echo "  run               - Run the app"
	@echo "  container-build   - Build app in containers and create container image"
	@echo "  container-run     - Run app container"
	@echo "  container-stop    - Stop app container"
	@echo "  container-logs    - Show app container logs"
	@echo "  container-destroy - Stop and delete app container, networks, volumes, and images"
	@echo "  help              - Show this help message"
