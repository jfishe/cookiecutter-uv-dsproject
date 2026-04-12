# cookiecutter-uv-dsproject

> A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that merges the
> **uv-first** tooling philosophy of
> [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) with the
> **data-science project layout** of
> [PyScaffold dsproject](https://github.com/pyscaffold/dsproject).

## Features

| Area | What you get |
|---|---|
| **Package manager** | `uv` — fast installs, deterministic lockfile, single `pyproject.toml` |
| **Build backend** | Hatchling with `src/` layout |
| **DS directories** | `data/{raw,interim,processed,external}`, `models/`, `notebooks/`, `reports/figures/`, `configs/`, `references/`, `scripts/` |
| **DS modules** | `dataset.py` · `features.py` · `modeling.py` — ready-made stubs |
| **Linting** | Ruff (lint + format), mypy (strict) |
| **CI** | GitHub Actions — lint → typecheck → test matrix (min + max Python) |
| **Release** | Trusted-publisher PyPI OIDC + GitHub Releases |
| **Docs** | Sphinx + MyST + Furo + autodoc2 (optional) |
| **Docker** | Multi-stage uv build, non-root user (optional) |
| **Pre-commit** | ruff, mypy, trailing-whitespace, end-of-file, YAML check |
| **Makefile** | install · fmt · lint · typecheck · test · jupyter · docs · docker · clean |

## Quickstart

```bash
# Install cookiecutter (if needed)
uv tool install cookiecutter

# Generate a project
cookiecutter gh:jfishe/cookiecutter-uv-dsproject

# The post-hook runs git init + uv sync automatically
cd my-ds-project
uv run pytest
```

## Template Variables

| Variable | Default | Description |
|---|---|---|
| `project_name` | `My DS Project` | Human-readable project name |
| `project_slug` | *(derived)* | Hyphenated, lowercase slug |
| `package_name` | *(derived)* | Python-importable name |
| `project_description` | — | One-line summary |
| `author_name` | — | Your full name |
| `author_email` | — | Your email |
| `github_username` | — | GitHub org or user |
| `python_version` | `3.12` | Target / CI ceiling version |
| `min_python_version` | `3.10` | `requires-python` floor |
| `license` | `MIT` | MIT · Apache-2.0 · BSD-3 · GPL-3 · Proprietary |
| `include_notebooks` | `yes` | Include `notebooks/` directory |
| `include_docs` | `yes` | Include `docs/` Sphinx scaffold |
| `include_docker` | `yes` | Include `Dockerfile` |
| `include_github_actions` | `yes` | Include `.github/workflows/` |
| `initial_version` | `0.1.0` | Starting version string |

## Generated Project Tree

```
my-ds-project/
├── src/my_ds_project/        ← installable package
│   ├── __init__.py
│   ├── dataset.py
│   ├── features.py
│   └── modeling.py
├── tests/
├── data/{raw,interim,processed,external}/
├── models/
├── notebooks/
├── reports/figures/
├── scripts/
├── references/
├── configs/
├── docs/
├── .github/workflows/
├── pyproject.toml
├── Makefile
├── Dockerfile
└── .pre-commit-config.yaml
```

## Development (on this template itself)

```bash
uv sync
uv run pytest tests/
```

## License

MIT
