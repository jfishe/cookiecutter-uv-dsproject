# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- markdownlint-disable MD024 -->

## [Unreleased]

These release notes summarize changes since `v3.0.0`.

### Added

- Added an opt-in `include_changelog` template option and a generated
  `CHANGELOG.md` scaffold that follows Keep a Changelog and Semantic
  Versioning.

### Fixed

- Fixed the generated package `__version__` export to read from
  `importlib.metadata`, keeping `pyproject.toml` as the single source of
  truth for the installed version.
- Fixed the generated `mirrors-mypy` hook to target `src/` explicitly
  when `pass_filenames: false` is enabled, so
  `prek run --all-files mypy` no longer fails with a missing-target
  error.
- Fixed the generated notebook display helper to satisfy the template's
  default mypy configuration, allowing freshly baked projects to pass
  their initial type-check run.
- Fixed the generated IPython profile config to keep the standard
  `get_config()` loader pattern, and configured Ruff to ignore `F821`
  for that file instead of requiring an explicit import.

## [v3.0.0]

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

### Fixed

- Fixed generated setup and docs instructions to consistently use the
  selected Python version during `uv sync`, avoiding version conflicts
  in freshly generated projects.

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

[unreleased]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v3.0.0...HEAD
[v3.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.1.0...v3.0.0
[v2.1.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v1.0.0...v2.0.0
