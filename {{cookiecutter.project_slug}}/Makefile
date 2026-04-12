.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help install fmt lint typecheck test jupyter docs docker-build clean

help: ## Show this help
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
				awk 'BEGIN {FS = ":.*?## "}; {printf "	\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies (uv sync --all-extras)
		uv sync --all-extras

fmt: ## Auto-format code with Ruff
		uv run ruff format src/ tests/
		uv run ruff check --fix src/ tests/

lint: ## Lint code with Ruff
		uv run ruff check src/ tests/
		uv run ruff format --check src/ tests/

typecheck: ## Type-check with mypy
		uv run mypy src/

test: ## Run tests with coverage
		uv run pytest --cov --cov-report=term-missing

jupyter: ## Launch JupyterLab
		uv run jupyter lab --notebook-dir=notebooks

docs: ## Build Sphinx docs
		uv run sphinx-build -b html docs/ docs/_build/html

docker-build: ## Build Docker image
		docker build -t {{ cookiecutter.project_slug }}:latest .

clean: ## Remove build artifacts and caches
		rm -rf dist/ build/ *.egg-info .venv/
		rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/
		rm -rf docs/_build/
		find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
		find . -type f -name "*.pyc" -delete 2>/dev/null || true
