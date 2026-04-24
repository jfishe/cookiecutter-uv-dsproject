# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
[![Python {{ cookiecutter.min_python_version }}+](https://img.shields.io/badge/python-{{ cookiecutter.min_python_version }}%2B-blue.svg)](https://www.python.org/downloads/)
{%- if cookiecutter.license != "Proprietary" %}
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/license-{{ cookiecutter.license | replace("-", "--") }}-green.svg)](LICENSE)
{%- endif %}

> {{ cookiecutter.project_description }}

## Project Layout

```
├── src/{{ cookiecutter.package_name }}/
│   ├── __init__.py
│   ├── py.typed               ← PEP 561 type-checking marker
│   ├── dataset.py             ← data loading & saving
│   ├── features.py            ← feature engineering
│   └── modeling.py            ← model persistence & metrics
├── tests/
│   ├── __init__.py
│   └── test_placeholder.py
├── data/
│   ├── raw/                   ← immutable original data
│   ├── interim/               ← intermediate transforms
│   ├── processed/             ← final, analysis-ready data
│   └── external/              ← third-party reference data
├── models/                    ← serialised models & metrics
├── notebooks/
│   └── getting-started.ipynb  ← starter notebook (dsproject-style)
├── reports/
│   └── figures/               ← generated plots
├── scripts/
│   └── train_model.py         ← CLI training entry point
├── configs/
│   └── example.yaml           ← experiment configuration template
├── references/                ← data dictionaries, papers, manuals
├── docs/                      ← Sphinx + MyST documentation
├── .github/workflows/         ← CI & release pipelines
├── pyproject.toml             ← single source of truth
├── Makefile                   ← common task shortcuts
├── Dockerfile                 ← multi-stage uv build
├── .pre-commit-config.yaml    ← ruff, mypy, standard hooks
│                                (includes pandas-stubs and joblib-stubs in dev)
├── .gitignore
├── LICENSE
└── README.md
```

## Quickstart

```bash
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtualenv & install all deps
make install          # or: uv sync --all-groups

# Run tests
make test             # or: uv run pytest

# Format & lint
make fmt lint
```

## Data Workflow

```python
from {{ cookiecutter.package_name }}.dataset import load_raw, save_processed
from {{ cookiecutter.package_name }}.features import build_features

df = load_raw("experiment_01.csv")
df = build_features(df)
save_processed(df, "experiment_01_features.parquet")
```
{%- if cookiecutter.include_notebooks == "yes" %}

## Notebooks

Launch JupyterLab with the project virtualenv kernel:

```bash
make jupyter
```
{%- endif %}
{%- if cookiecutter.include_docs == "yes" %}

## Documentation

```bash
make docs             # builds to docs/_build/html/
```
{%- endif %}

## Makefile Targets

| Target | Description |
|---|---|
| `install` | `uv sync --all-groups` |
| `fmt` | Auto-format with Ruff (installs dev group if needed) |
| `lint` | Lint with Ruff (installs dev group if needed) |
| `typecheck` | Run mypy (ensure dev group installed) |
| `test` | Run pytest with coverage (ensure dev group installed) |
| `jupyter` | Launch JupyterLab (syncs notebooks group) |
| `docs` | Build Sphinx docs (syncs docs group) |
| `docker-build` | Build Docker image |
| `clean` | Remove caches & build artifacts |

## Contributing

1. Fork & clone
2. `make install`
3. Create a feature branch
4. `make fmt lint typecheck test`
5. Open a pull request

## License

{%- if cookiecutter.license == "Proprietary" %}
Proprietary — see [LICENSE](LICENSE).
{%- else %}
[{{ cookiecutter.license }}](LICENSE)
{%- endif %}
