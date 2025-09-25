VENV_DIR := .venv/PY-VENV
REQUIREMENTS_FILE := requirements.txt

.PHONY: init dev format lint help

init: $(REQUIREMENTS_FILE)
	@ln -sf $(CURDIR)/.hooks/pre-commit.sh .git/hooks/pre-commit
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
	fi
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)

dev:
	@. $(VENV_DIR)/bin/activate && uvicorn app.main:app --reload

format:
	@. $(VENV_DIR)/bin/activate && \
	ruff format --force-exclude -- app

lint:
	@. $(VENV_DIR)/bin/activate && \
	ruff check --force-exclude -- app && \
	mypy --pretty -- app

help:
	@echo "Available targets:"
	@echo "  init          - Set up py venv and install requirements"
	@echo "  dev           - Start app in development mode"
	@echo "  lint          - Run lint on all python files"
	@echo "  format        - Run format on all python files"
	@echo "  help          - Show this help message"
