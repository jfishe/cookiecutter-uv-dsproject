# {{ cookiecutter.project_name }}

<!-- docs:badges:start -->
[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
[![Python {{ cookiecutter.min_python_version }}+](https://img.shields.io/badge/python-{{ cookiecutter.min_python_version }}%2B-blue.svg)](https://www.python.org/downloads/)
{%- if cookiecutter.license != "Proprietary" %}
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/license-{{ cookiecutter.license | replace("-", "--") }}-green.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/blob/main/LICENSE)
{%- endif %}
<!-- docs:badges:end -->

> {{ cookiecutter.project_description }}

## Project Layout

```text
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
{%- if cookiecutter.include_notebooks == "yes" and cookiecutter.include_notebook_ux == "yes" %}
├── .ipython/
│   └── profile_default/
│       └── ipython_config.py  ← project-local JupyterLab inspector config
{%- endif %}
├── reports/
│   └── figures/               ← generated plots
├── scripts/
│   └── train_model.py         ← CLI training entry point
├── configs/
│   └── example.yaml           ← experiment configuration template
├── references/                ← data dictionaries, papers, manuals
├── docs/                      ← Sphinx + MyST documentation
├── .readthedocs.yaml          ← Read the Docs build config
├── .github/workflows/         ← CI & release pipelines
├── pyproject.toml             ← single source of truth
├── Makefile                   ← common task shortcuts
{%- if cookiecutter.include_docker == "yes" %}
├── Dockerfile                 ← multi-stage uv build
{%- endif %}
{%- if cookiecutter.pre_commit_tool != "none" %}
├── .pre-commit-config.yaml    ← ruff, {{ cookiecutter.type_checker }}, standard hooks
{%- if cookiecutter.type_checker == "mypy" %}
│                                (includes pandas-stubs and joblib-stubs in dev)
{%- endif %}
{%- endif %}
├── .gitignore
├── LICENSE
└── README.md
```

## Quickstart

```bash
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a {{ cookiecutter.python_version }} virtualenv & install all deps
make install          # or: uv sync --python {{ cookiecutter.python_version }} --all-groups

# Run tests
make test             # or: uv run pytest

# Format & lint
make fmt lint
```

{%- if cookiecutter.pre_commit_tool != "none" %}

## Git Hooks

The generated project includes a `.pre-commit-config.yaml` for
{%- if cookiecutter.pre_commit_tool == "prek" %}
[`prek`](https://github.com/j178/prek), a faster drop-in replacement for
`pre-commit`.
{%- else %}
[`pre-commit`](https://pre-commit.com/).
{%- endif %}

```bash
# Install Git hooks and prepare hook environments
uv run {{ cookiecutter.pre_commit_tool }} install --prepare-hooks -f

# Run all configured hooks on demand
uv run {{ cookiecutter.pre_commit_tool }} run --all-files
```
{%- endif %}

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

{%- if cookiecutter.include_notebook_ux == "yes" %}
The generated project also enables richer JupyterLab inspector help
with a project-local IPython config and `docrepr`.
Open the inspector with `Ctrl+I` (`Cmd+I` on macOS) for HTML-rendered
docstrings while you type.
{%- endif %}
The notebooks dependency group also includes `nbdime` for notebook-aware
diff and merge tooling in Jupyter and Git workflows.
For nbconvert-friendly tables, use the generated display helper:

```python
from {{ cookiecutter.package_name }}.display import display_dataframe

display_dataframe(
    df.describe(),
    caption="Summary statistics",
    label="tab:summary-statistics",
)
```

It renders HTML in JupyterLab and provides LaTeX output for notebook
exports such as `nbconvert --to pdf`.
To preserve table captions and labels in PDF exports, use the bundled
nbconvert LaTeX template:

```bash
jupyter nbconvert --to=pdf --template=templates/latex \
  notebooks/getting-started.ipynb --output-dir=reports
```

Notebook-level export settings live under `metadata.latex_export`.
The bundled template reads `document_id`, `revision`, and `page_prefix`
from that block to build a right-aligned running header and optional
page-number prefix:

```json
{
  "title": "My DS Project getting started",
  "latex_export": {
    "document_id": "DOC-0001",
    "revision": "0",
    "page_prefix": "A-"
  }
}
```
{%- endif %}
{%- if cookiecutter.include_docs == "yes" %}

## Documentation

```bash
make docs             # builds to docs/_build/html/
make latexpdf         # builds docs/_build/latex/*.pdf
```

Read the Docs can use the bundled `.readthedocs.yaml`, which installs the
`docs` dependency group with
`uv sync --python {{ cookiecutter.python_version }} --group docs`
and points RTD at `docs/conf.py`.

To build PDF docs, install a TeX toolchain first.
On Debian or Ubuntu, the minimum packages are typically:

```bash
sudo apt install latexmk texlive-xetex xindy
```

Then run:

```bash
make latexpdf
make -C docs clean    # removes Sphinx build artifacts
```
{%- endif %}

## Makefile Targets

| Target | Description |
|---|---|
| `install` | `uv python install {{ cookiecutter.python_version }} && uv sync --python {{ cookiecutter.python_version }} --all-groups` |
| `fmt` | Auto-format with Ruff (installs dev group if needed) |
| `lint` | Lint with Ruff (installs dev group if needed) |
| `typecheck` | Run {{ cookiecutter.type_checker }} (ensure dev group installed) |
| `test` | Run pytest with coverage (ensure dev group installed) |
{%- if cookiecutter.pre_commit_tool != "none" %}
| `uv run {{ cookiecutter.pre_commit_tool }} install --prepare-hooks -f` | Install Git hooks and prepare hook environments |
| `uv run {{ cookiecutter.pre_commit_tool }} run --all-files` | Run the configured hooks across the repo |
{%- endif %}
| `jupyter` | Launch JupyterLab (syncs notebooks group{% if cookiecutter.include_notebook_ux == "yes" %} and enables rich inspector help{% endif %}) |
| `docs` | Build Sphinx docs (syncs docs group) |
| `latexpdf` | Build Sphinx PDF docs (syncs docs group) |
| `docker-build` | Build Docker image |
| `clean` | Remove caches & build artifacts |

## Contributing

1. Fork & clone
2. `make install`
3. Create a feature branch
{%- if cookiecutter.pre_commit_tool != "none" %}
4. `uv run {{ cookiecutter.pre_commit_tool }} run --all-files`
5. `make fmt lint typecheck test`
6. Open a pull request
{%- else %}
4. `make fmt lint typecheck test`
5. Open a pull request
{%- endif %}

## License

{%- if cookiecutter.license == "Proprietary" %}
Proprietary — see the repository license file.
{%- else %}
[{{ cookiecutter.license }}](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/blob/main/LICENSE)
{%- endif %}
