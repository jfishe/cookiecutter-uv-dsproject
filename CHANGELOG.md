# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

These release notes summarize changes since `v1.0.0`.

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

### Fixed

- Fixed PDF docs builds by excluding README badge images from the docs
  include while preserving the top-level README heading.
- Fixed generated docs workflows so `make docs`, `make latexpdf`, and
  `make -C docs clean` all work as documented.
- Fixed notebook PDF export so table captions and labels survive
  nbconvert's default LaTeX caption suppression.

[Unreleased]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v1.0.0...HEAD
