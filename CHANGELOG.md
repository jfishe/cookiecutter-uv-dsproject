# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and
this project adheres to [Semantic Versioning].

<!-- markdownlint-disable MD024 -->

## [Unreleased]

<!-- ### Added -->

<!-- ### Changed -->

<!-- ### Deprecated -->

<!-- ### Removed -->

<!-- ### Fixed -->

<!-- ### Security -->

### Added

- Generated hooks: rumdl (`rumdl-check --fix`) lints Markdown, with
  `[tool.rumdl]` in `pyproject.toml` and the MyST flavor for `docs/`.
- Generated hooks: actionlint and zizmor (`--offline`) check workflow files
  when `include_github_actions` is `yes`.
- Generated Dependabot config tracks hook revs (`pre-commit` ecosystem).

### Changed

- Generated hooks: rumdl and ruff-format (which now formats Python code
  blocks in Markdown) replace markdownlint-cli and mdformat, so hooks no
  longer need Node.
- Generated hooks: `prek` projects use prek's `repo: builtin` hooks for the
  standard file checks; ruff hooks use the `ruff-check` id; hook revs bumped
  (pre-commit-hooks v6.0.0, ruff v0.17.3, mirrors-mypy v2.3.1,
  pyproject-fmt v2.30.3).
- Generated CI: the lint job runs every hook (`uv run <tool> run
  --all-files`) instead of ruff alone; `astral-sh/setup-uv` bumped to
  v10.3.0.
- Generated Dependabot config uses the `uv` ecosystem instead of `pip`.
- Generated `pyproject.toml`: floors `ruff>=0.16` and `prek>=0.5`; layout
  matches pyproject-fmt v2.30 (sorted dev group, Python 3.15 classifier,
  flattened `[tool.ty]`).

### Fixed

- Generated CI: the test matrix no longer lists the same Python twice when
  `python_version` equals `min_python_version` (actionlint error).
- Generated `display.py`: drop an implicit f-string concatenation that
  ruff-format rewrote on every run.
- CI: release notes extraction pulled in every changelog section back to a
  stale "previous tag" instead of just the current release, because the
  repo's tag history mixes `v`-prefixed and unprefixed tags and git's
  version-sort does not order them chronologically. Extraction now isolates
  the current release's heading directly instead of relying on a computed
  previous tag.

## [v4.2.0]

### Added

- `make audit` to run `uv audit` and [zizmor].

### Changed

- Move `CLAUDE.md` to `.claude/` in template and root.

### Fixed

- Align `pyproject.toml` version with Changelog.
- Only include LaTeX nbconvert templates with notebooks.
- CI: changelog heading missed tags.

### Security

- Add cool down period for dependencies.
- CI: pin dependencies with SHAs.
- CI: Do not persist credentials.
- CI: Restrict permissions to read.
- CI: Prevent cache poisoning by not caching uv.
- CI: Replace template expansion with environment variables.
- CI: Manage concurrency so releases don't clobber each other.

## [v4.1.0]

### Added

- An adapted [CLAUDE.md template] for the template and root.
- `pyrefly` as a third type_checker option (alongside `mypy` and `ty`)
- `pytest` strict-config to template and root
- Sphinx documents include Changelog.

### Changed

- BUILD: configure hatchling for dynamic versioning per
  [Python Developers Tooling Handbook].
- DOCS: initial_version seeded in Changelog only.
- CI: trigger release only on semver tags.

### Fixed

DOCS: add missing version URLs.

### Removed

`pytest` does not require `tests/__init__.py` for discovery.

## [v4.0.0]

### Added

- Dependabot Action to update GitHub Action.
- Ignore `direnv` files.

### Changed

- CI: update versions.
- CI: narrow read and write permission to specific jobs.

### Fixed

- CI: should not generate a blank release when Sigstore fails.
- PyProject version 4.0.0 matches Changelog. Added author.

## [v3.0.3]

### Added

GitHub Action automating release.

## [v3.0.1]

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
- Changed default minimum version to Python 3.12 because
  Numpy typing is not compatible with mypy or ty
  `python_version=3.10`.

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

[claude.md template]: https://pydevtools.com/handbook/how-to/how-to-use-the-pydevtools-claude-md-template/
[keep a changelog]: https://keepachangelog.com/en/1.1.0/
[python developers tooling handbook]: https://pydevtools.com/handbook/how-to/how-to-add-dynamic-versioning-to-uv-projects/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
[unreleased]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/4.2.0...HEAD
[v2.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v1.0.0...v2.0.0
[v2.1.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.0.0...v2.1.0
[v3.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v2.1.0...v3.0.0
[v3.0.1]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v3.0.0...v3.0.1
[v3.0.3]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/v3.0.1...3.0.3
[v4.0.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/3.0.3...4.0.0
[v4.1.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/4.0.0...4.1.0
[v4.2.0]: https://github.com/jfishe/cookiecutter-uv-dsproject/compare/4.1.0...4.2.0
[zizmor]: https://docs.zizmor.sh/
