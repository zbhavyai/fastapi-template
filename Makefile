VENV_DIR := .venv/PY-VENV
REQUIREMENTS_FILE := requirements.txt

.PHONY: prep dev format lint run help

prep: $(REQUIREMENTS_FILE)
	@ln -sf $(CURDIR)/.hooks/pre-commit.sh .git/hooks/pre-commit
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
	fi
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)

dev:
	@. $(VENV_DIR)/bin/activate && fastapi dev app/main.py

format:
	@. $(VENV_DIR)/bin/activate && \
	ruff format --force-exclude -- app

lint:
	@. $(VENV_DIR)/bin/activate && \
	ruff check --force-exclude -- app && \
	mypy --pretty -- app

run:
	@. $(VENV_DIR)/bin/activate && fastapi run app/main.py

help:
	@echo "Available targets:"
	@echo "  prep          - Set up py venv and install requirements"
	@echo "  dev           - Start app in development mode"
	@echo "  lint          - Run lint on all python files"
	@echo "  format        - Run format on all python files"
	@echo "  run           - Run the app"
	@echo "  help          - Show this help message"
