.DEFAULT_GOAL := help
SHELL := /bin/bash

# Ensure tools from the selected Python version are available when
# running code-quality and test targets. Use uv sync --group to
# install only the needed groups quickly.
UV_PROJECT_PYTHON ?= {{ cookiecutter.python_version }}
UV_SYNC ?= uv sync --python $(UV_PROJECT_PYTHON)
UV_SYNC_DEV ?= $(UV_SYNC) --group dev

.PHONY: help install fmt lint typecheck test jupyter docs latexpdf clean
{%- if cookiecutter.include_docker == "yes" %}
.PHONY: docker-build
{%- endif %}

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependency-groups
	uv python install $(UV_PROJECT_PYTHON)
	$(UV_SYNC) --all-groups

fmt: ## Auto-format code with Ruff (ensure dev tools installed)
	$(UV_SYNC_DEV)
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

lint: ## Lint code with Ruff (ensure dev tools installed)
	$(UV_SYNC_DEV)
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

typecheck: ## Type-check with {{ cookiecutter.type_checker }} (ensure dev tools installed)
	$(UV_SYNC_DEV)
{%- if cookiecutter.type_checker == "mypy" %}
	uv run mypy src/
{%- else %}
	uv run ty check src/
{%- endif %}

test: ## Run tests with coverage (ensure dev tools installed)
	$(UV_SYNC_DEV)
	uv run pytest --cov --cov-report=term-missing

jupyter: ## Launch JupyterLab (will try to install notebooks group)
	$(UV_SYNC) --group notebooks || true
{%- if cookiecutter.include_notebooks == "yes" and cookiecutter.include_notebook_ux == "yes" %}
	IPYTHONDIR=.ipython uv run jupyter lab --notebook-dir=notebooks
{%- else %}
	uv run jupyter lab --notebook-dir=notebooks
{%- endif %}

docs: ## Build Sphinx docs (ensure docs group installed)
	$(MAKE) -C docs html

latexpdf: ## Build Sphinx PDF docs (ensure docs group installed)
	$(MAKE) -C docs latexpdf

{%- if cookiecutter.include_docker == "yes" %}
docker-build: ## Build Docker image
	docker build -t {{ cookiecutter.project_slug }}:latest .
{%- endif %}

clean: ## Remove build artifacts and caches
	rm -rf dist/ build/ *.egg-info .venv/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ .ty_cache/ htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
