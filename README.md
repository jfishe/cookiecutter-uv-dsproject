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

- Notebook UX

  - Optional JupyterLab inspector enhancements with `docrepr`
    and a project-local IPython config.
  - Inspired by Martin Renou's
    ["Inspector JupyterLab"](https://blog.jupyter.org/inspector-jupyterlab-404cce3e1df6)
    on the Jupyter Blog.
  - Notebook projects include `nbdime` for notebook-aware diff and
    merge tooling.

- Linting

  - Ruff (lint + format) plus configurable type checking with
    mypy or ty.

- CI

  - GitHub Actions — lint → typecheck → tests (Python matrix).

- Release

  - Trusted-publisher PyPI OIDC and GitHub Releases (optional).

- Docs

  - Sphinx + MyST + Furo + autodoc2 (optional).
  - Generated projects include a `.readthedocs.yaml` that builds docs with
    `uv sync --python <selected-version> --group docs`.
  - PDF output via Sphinx LaTeX requires a TeX toolchain such as
    `latexmk`, `texlive-xetex`, and `xindy`.

- Docker

  - Multi-stage uv build, non-root user (optional).

- Git hooks

  - Optional `.pre-commit-config.yaml` support with
    `pre_commit_tool: prek` (default), `pre-commit`, or `none`.
  - Generated projects add the matching runner to the `dev`
    dependency group unless `none` is selected.
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

    - `mirrors-mypy` with `pandas-stubs` and
      `--config-file=pyproject.toml`, or a local `ty` hook via
      `uv run ty check src/`.

  - Type checking options

    - The default `mypy` option installs `pandas-stubs` and
      `joblib-stubs` in the `dev` dependency-group so mypy can
      type-check commonly used DS libraries.

    - The `ty` option installs `ty` plus `joblib` in the `dev`
      dependency-group and adds a minimal `[tool.ty]` configuration
      scoped to `src/`.

    - If you add libraries without upstream typing, prefer
      installing third-party stub packages (e.g.,
      `types-<pkg>` or `<pkg>-stubs`) into the `dev` group.

    - To run type checks locally, ensure the `dev` group is
      installed first with the selected Python version, for example
      `uv sync --python <selected-version> --group dev`, or use
      `make typecheck`.

- Makefile

  - install, fmt, lint, typecheck, test, jupyter, docs, docker,
    clean.

## Quickstart

```bash
# Install cookiecutter (if needed)
uv tool install cookiecutter

# Generate a project
cookiecutter gh:jfishe/cookiecutter-uv-dsproject

# The post-hook runs git init + uv sync with the selected Python automatically
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

- type_checker: `mypy`/`ty` — Static type checker for optional Git
  hooks, `make typecheck`, and CI.

- license: `MIT` (choices include Apache-2.0, BSD-3, GPL-3,
  Proprietary).

- include_notebooks / include_docs / include_docker /
  include_github_actions: `yes`/`no` flags that control optional
  features.

- pre_commit_tool: `prek`/`pre-commit`/`none` — choose the generated
  Git hook runner, with `prek` as the default.

- include_notebook_ux: `yes`/`no` — when notebooks are enabled,
  configure richer JupyterLab inspector help with `docrepr`
  and a project-local IPython profile.

- initial_version: `0.1.0` — Starting version string.

## Generated project tree

```text
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
├── .ipython/
│   └── profile_default/
│       └── ipython_config.py
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
├── .readthedocs.yaml
├── pyproject.toml
├── Makefile
├── Dockerfile
├── .pre-commit-config.yaml    # optional; generated unless runner=none
├── .gitignore
├── LICENSE
└── README.md
```

## Development (on this template)

```bash
uv sync
uv run pytest tests/
```

## PDF docs dependencies

Generated projects can build HTML docs with `make docs`.
To build PDF docs with Sphinx's LaTeX builder, install a TeX
toolchain first.

On Debian or Ubuntu, the minimum packages are typically:

```bash
sudo apt install latexmk texlive-xetex xindy
```

Then build the PDF with:

```bash
cd my-ds-project
make latexpdf
make -C docs clean
```

## License

MIT
