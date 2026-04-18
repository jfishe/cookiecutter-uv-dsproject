# Copilot instructions for cookiecutter-uv-dsproject

Purpose

This file helps future Copilot sessions understand the template
layout, common tooling, and typical commands for generated projects.

1. Build, test, and lint commands

Install and sync the project environment (uses uv).

uv sync

Run the full test suite (via the uv runner).

uv run pytest

Run a single test using pytest node selection.

uv run pytest tests/<path_to_test>::<test_name>

or

uv run pytest -k "<substring_of_test_name>"

Lint, format, and typecheck. This template uses ruff and mypy.

uv run ruff .

uv run mypy src

Makefile targets are provided in generated projects and mirror
many uv commands.

make test

make lint

make typecheck

make fmt

make docs

2. High-level architecture (generated project)

Packaging

Uses src/ layout with a package at src/<package_name>.

A py.typed file is included to indicate the package is typed.

Tooling

This template prefers the "uv" package manager.

uv produces a deterministic uv.lock and exposes uv run to
execute tools inside the project environment.

Data-science layout

Top-level directories include:

- data/{raw,interim,processed,external}
- models/
- notebooks/
- reports/figures/
- scripts/
- configs/
- references/

Code scaffold

Minimal DS modules are placed under src/<package_name> and
include dataset.py, features.py, and modeling.py as starter
stubs.

CI and release

When enabled, .github/workflows/ contains CI that runs:

lint → typecheck → tests

Release workflows are included when the template option for
releases is selected.

3. Key conventions and repo-specific patterns

Template vs generated project

This repository is a Cookiecutter template.

Files under hooks/ (for example, pre_gen_project.py and
post_gen_project.py) run during generation and should not be
treated as runtime project code.

"uv" first

Prefer uv sync and uv run \<tool\> over global installs.

uv ensures reproducible installs and a lockfile.

Strict typing and linting

Generated projects use ruff for linting/formatting and mypy for
static typing.

Expect stricter type coverage than many data-science templates.

Makefile and uv parity

Many CI and developer commands are available via both the
Makefile and uv run. Use uv run to reproduce CI-like runs.

Template flags

Some features are optional and controlled by template flags:

- include_notebooks
- include_docs
- include_docker
- include_github_actions

Generated projects may omit files for disabled features.

Tests

pytest is the test runner.

A placeholder test exists in this template. Use pytest node
syntax to execute specific tests.

4. Files to consult when making automation/AI edits

- README.md — quickstart, Makefile target list, and generated
  tree.
- pyproject.toml — build backend, dependency-groups, and dev
  tool declarations.
- hooks/ — cookiecutter hooks that affect the generated
  repository state.
- .pre-commit-config.yaml — pre-commit hooks used by generated
  projects (ruff, mypy, etc.).

5. AI/assistant config scan

No existing Copilot/Claude/Cursor/Jules/Windsurf/Aider/Cline
assistant rules were found in this template.

If adding assistant-specific rules, place them at the repo root
or under .github/ and update this file.

Formatting preferences

- Markdown: prefer semantic line breaks. Wrap lines at ~80
  characters and keep one sentence per line to improve diffs
  and AI editing.

- Markdownlint: follow common rules. Examples:
  - MD013: line length — wrap at ~80 characters.
  - MD022/MD024: headings — ensure consistent heading levels
    and avoid duplicate headings.
  - MD041: first line should be a top-level heading.

Commit message conventions

Follow Conventional Commits:

<https://www.conventionalcommits.org/en/v1.0.0/>

Keep the subject to a maximum of 50 characters.

Wrap body and footer lines at 72 characters.

Example template (include a short machine-readable id on the
first line):

```gitcommit
# id:<id> <type>(<scope>): (If applied, this commit will)
# <subject>

# id:12345 feat(login): add password enforcement

# |<---- Subject is maximum 50 Characters  ---->|

# <body>

# |<---- Try To Limit Each Line to a Maximum Of 72 # Characters ---->|

# <footer>

# |<---- Try To Limit Each Line to a Maximum Of 72 # Characters ---->|
```

Types

- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the
  code (white-space, formatting, etc.)
- refactor: A code change that neither fixes a bug nor adds
  a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- build: Changes that affect the build system or external
  deps
- ci: Changes to Continuous Integration
- chore: Other changes that don't modify src or test files
- revert: Undo changes

Footer guidance

The footer should contain any information about breaking
changes.

Start a breaking change note with the words:

BREAKING CHANGE:

Follow with a short description and additional details as
needed.
