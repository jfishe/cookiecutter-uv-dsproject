# Python Project Rules

<!-- markdownlint-disable MD013 -->

<!-- Adapted from pydevtools.com, the Python Developer Tooling Handbook, for -->

<!-- this project's own selected tooling (see cookiecutter-uv-dsproject). -->

<!-- Full explanations: https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/ -->

## Package management

This project uses uv. Do not use pip, pip-tools, poetry, or conda.

- Add runtime dependency: `uv add <package>` (writes to `[project.dependencies]`)
- Add dev dependency: `uv add --dev <package>` (writes to `[dependency-groups]` per PEP 735)
- Remove dependency: `uv remove <package>`
- Sync environment from lockfile: `uv sync`
- Regenerate lockfile from constraints: `uv lock`
- Upgrade locked versions: `uv lock --upgrade`
- Commit `uv.lock` to version control (current uv guidance is to commit it for applications, CLIs, and libraries)

## Running code

Always use `uv run` to execute Python code and tools. Never call `python`, `pytest`, `ruff`, or other tools directly. They may not resolve to the project's virtual environment.

- Run a script: `uv run python script.py`
- Run a module: `uv run python -m module_name`
- Run a tool: `uv run pytest`, `uv run ruff check .`
- One-off tool (not a project dependency): `uvx <tool>`

## Creating new projects

- Application or script: `uv init project-name`
- Library or distributable package: `uv init --package project-name`
- Always use `pyproject.toml` for metadata (PEP 621). Never create `setup.py`, `setup.cfg`, or `requirements.txt`.

## Testing

- Framework: pytest
- Run tests: `uv run pytest`
- Test files go in `tests/` at the project root
- Test file naming: `test_*.py`
- Test function naming: `test_*`
- No `__init__.py` needed in `tests/`

## Linting and formatting

- Tool: ruff (handles both linting and formatting)
- Lint: `uv run ruff check .`
- Lint and auto-fix: `uv run ruff check --fix .`
- Format: `uv run ruff format .`
- Check formatting: `uv run ruff format --check .`
- Configuration lives in `pyproject.toml` under `[tool.ruff]`

## Type checking
{% if cookiecutter.type_checker == "mypy" %}
- Tool: mypy
- Run: `uv run mypy .`
- Configuration lives in `pyproject.toml` under `[tool.mypy]`
{%- else %}
- Tool: ty
- Run: `uv run ty check`
- Configuration lives in `pyproject.toml` under `[tool.ty]`
{%- endif %}

## Code style

- Follow ruff's defaults for formatting (88 char line length, double quotes, spaces)
- Import sorting is handled by ruff (`isort` rules enabled via `select = ["I"]`)
- Do not add `# type: ignore` comments without an error code
{%- if cookiecutter.pre_commit_tool != "none" %}

## Pre-commit hooks

- Tool: {{ cookiecutter.pre_commit_tool }}, pinned as a dev dependency — always invoke via `uv run`, never `uvx` or a global install
- Install hooks: `uv run {{ cookiecutter.pre_commit_tool }} install --prepare-hooks -f`
- Run all hooks on demand: `uv run {{ cookiecutter.pre_commit_tool }} run --all-files`
{%- endif %}

## What NOT to do

- Do not create or activate virtual environments manually. uv manages `.venv/` automatically.
- Do not install packages globally or with `pip install`.
- Do not create `requirements.txt` for dependency management. Use `pyproject.toml` and `uv.lock`.
- Do not run `python setup.py` commands.
- Do not add dependencies to pyproject.toml by hand. Use `uv add`.
- If you must edit pyproject.toml directly, write dev dependencies under `[dependency-groups]` (PEP 735), not the legacy `[tool.uv.dev-dependencies]` table.

## Project-specific rules
