# cookiecutter-uv-dsproject

> A [Cookiecutter](https://cookiecutter.readthedocs.io/)
> template that merges the
> **uv-first** tooling philosophy of
> [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv)
> with the **data-science project layout** of
> [PyScaffold dsproject](https://github.com/pyscaffold/dsproject).

## Features

- Package manager

  - `uv` — fast installs, deterministic lockfile, single
    `pyproject.toml`.

- Build backend

  - Hatchling with `src/` layout.

- Data-science directories

  - `data/{raw,interim,processed,external}`
  - `models/`
  - `notebooks/`
  - `reports/figures/`
  - `configs/`, `references/`, `scripts/`

- DS modules

  - `dataset.py`, `features.py`, `modeling.py` — starter stubs.

- Linting

  - Ruff (lint + format) and mypy (strict).

- CI

  - GitHub Actions — lint → typecheck → tests (Python matrix).

- Release

  - Trusted-publisher PyPI OIDC and GitHub Releases (optional).

- Docs

  - Sphinx + MyST + Furo + autodoc2 (optional).

- Docker

  - Multi-stage uv build, non-root user (optional).

- Pre-commit

  - Configured hooks include:

    - pre-commit-hooks (trailing-whitespace, end-of-file,
      check-yaml, mixed-line-ending, check-ast, check-json,
      check-toml).

    - pyproject-fmt (pyproject formatting).

    - ruff with auto-fix enabled (`--fix`, `--show-fixes`,
      `--exit-non-zero-on-fix`) and ruff-format for files.

    - markdownlint-fix and mdformat (with front-matters,
      gfm, pyproject, ruff, footnote plugins).

    - gitlint on commit-msg for Conventional Commits.

    - mirrors-mypy with `pandas-stubs` and
      `--config-file=pyproject.toml`.

  - Type stubs and mypy

    - The template installs `pandas-stubs` and `joblib-stubs` in
      the `dev` dependency-group so mypy can type-check commonly
      used DS libraries.

    - If you add libraries without upstream typing, prefer
      installing third-party stub packages (e.g.,
      `types-<pkg>` or `<pkg>-stubs`) into the `dev` group.

    - To run type checks locally, ensure the `dev` group is
      installed first: `uv sync --group dev` or `make typecheck`.

- Makefile

  - install, fmt, lint, typecheck, test, jupyter, docs, docker,
    clean.

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

## Template variables

- project_name: `My DS Project` — Human-readable project name.

- project_slug: derived — Hyphenated, lowercase slug.

- package_name: derived — Python-importable name.

- project_description: — One-line summary.

- author_name / author_email: — Author contact info.

- github_username: — GitHub org or user.

- python_version: `3.12` — Target / CI ceiling version.

- min_python_version: `3.10` — `requires-python` floor.

- license: `MIT` (choices include Apache-2.0, BSD-3, GPL-3,
  Proprietary).

- include_notebooks / include_docs / include_docker /
  include_github_actions: `yes`/`no` flags that control optional
  features.

- initial_version: `0.1.0` — Starting version string.

## Generated project tree

```
my-ds-project/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── src/my_ds_project/
│   ├── __init__.py
│   ├── py.typed
│   ├── dataset.py
│   ├── features.py
│   └── modeling.py
├── tests/
│   ├── __init__.py
│   └── test_placeholder.py
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── models/
├── notebooks/
│   └── getting-started.ipynb
├── reports/
│   └── figures/
├── scripts/
│   └── train_model.py
├── configs/
│   └── example.yaml
├── references/
├── docs/
│   ├── conf.py
│   ├── index.md
│   └── api/
│       └── index.md
├── pyproject.toml
├── Makefile
├── Dockerfile
├── .pre-commit-config.yaml
├── .gitignore
├── LICENSE
└── README.md
```

## Development (on this template)

```bash
uv sync
uv run pytest tests/
```

## License

MIT
