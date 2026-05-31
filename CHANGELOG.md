# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

These release notes summarize changes since `v2.1.0`.

### Changed

- Replaced the old yes/no hook toggle with a `pre_commit_tool`
  template option supporting `prek` (default), `pre-commit`, or
  `none`, and now only generate `.pre-commit-config.yaml` when a
  runner is selected.

### BREAKING CHANGE

- Replaced `include_pre_commit` with `pre_commit_tool`, so existing
  Cookiecutter `--replay` data and saved contexts using the old
  variable will no longer render without updating that setting.

## [v2.1.0]

### Fixed

Updated version in `pyproject.toml`.

## [v2.0.0]

### Added

- Added an optional `ty` type-checker template choice and wired it
  through generated project dependencies, pre-commit hooks, Makefile
  targets, and CI.
- Added optional JupyterLab inspector enhancements with a project-local
  IPython configuration for notebook-focused projects.
- Added nbconvert-friendly DataFrame display helpers in
  `src/<package_name>/display.py` so generated notebooks can emit HTML,
  plain-text, and LaTeX table output.
- Added a custom nbconvert LaTeX template under `templates/latex/` to
  restore captions for both `table` and `longtable` output.
- Added a generated `docs/Makefile` plus top-level `make latexpdf`
  support for Sphinx documentation builds.
- Added a generated `.readthedocs.yaml` so projects with docs enabled can
  build on Read the Docs via `uv sync --group docs` and `docs/conf.py`.

### Changed

- Expanded the generated Sphinx configuration with richer MyST support,
  explicit LaTeX settings, and XeLaTeX as the PDF engine.
- Standardized generated projects on NumPy-style docstrings across the
  docs stack and Ruff's pydocstyle checks.
- Updated generated README and docs guidance to document Debian/Ubuntu
  TeX dependencies for PDF docs, including `latexmk`, `texlive-xetex`,
  and `xindy`.
- Updated the starter notebook to demonstrate notebook metadata,
  table-export metadata, LaTeX cross-references via
  `\autoref{tab:example-notebook-summary}`, and the new display helper
  workflow.
- Updated the generated nbconvert LaTeX template to read optional
  `latex_export` notebook metadata for document IDs, revisions, and
  page-number prefixes in running headers.

### Fixed

- Fixed PDF docs builds by excluding README badge images from the docs
  include while preserving the top-level README heading.
- Fixed generated docs workflows so `make docs`, `make latexpdf`, and
  `make -C docs clean` all work as documented.
- Fixed notebook PDF export so table captions and labels survive
  nbconvert's default LaTeX caption suppression.
- Fixed the generated Makefile so the `docker-build` target is only
  included when Docker support is enabled.

[Unreleased]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.1.0...HEAD
[v2.1.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v1.0.0...v2.0.0
