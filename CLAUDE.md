# cookiecutter-uv-dsproject — maintainer notes

This repo *is* a cookiecutter template, not a Python application. The only
"real" Python package here is the test suite; everything under
`{{cookiecutter.project_slug}}/` is Jinja source that renders into someone
else's project. Treat the two halves differently.

## Layout

- `cookiecutter.json` — the prompted variables and their defaults/choices.
  Any new variable must be added here first.
- `{{cookiecutter.project_slug}}/` — the template body. File and directory
  names, and file contents, are Jinja2 templates rendered with the
  `cookiecutter.*` context.
- `hooks/pre_gen_project.py` — runs before rendering; validates
  `project_slug` / `package_name` (regex + reserved-word checks) and aborts
  the bake on failure.
- `hooks/post_gen_project.py` — runs after rendering; deletes files/dirs for
  disabled features (`prune_features`), then `git init`s and `uv sync`s the
  generated project.
- `tests/test_bake_project.py` — bakes the template with `pytest-cookies`
  under many option combinations and asserts on the *generated* output.

## Editing templated files

- Every conditional feature (`include_notebooks`, `include_docs`,
  `include_docker`, `include_github_actions`, `include_changelog`,
  `pre_commit_tool`, `type_checker`, …) must be reflected consistently in
  **three** places, or the generated project will contain dead references:
  1. The Jinja `{%- if %}` blocks in the templated files themselves
     (`pyproject.toml`, `README.md`, `CLAUDE.md`, etc.)
  2. `hooks/post_gen_project.py::prune_features` if the feature adds files
     that must be deleted when disabled (not just made conditional inline)
  3. A bake test in `tests/test_bake_project.py` exercising both the
     enabled and disabled/alternate states
- Jinja whitespace control: this project's files mix headings with
  conditional bodies (see `{{cookiecutter.project_slug}}/CLAUDE.md`'s
  "Type checking" section). `{%- if %}` trims the newline *before* the tag,
  which will eat a deliberate blank line if placed directly under a
  heading — prefer a bare `{% if %}` there and trim on the closing tag
  instead. Always re-bake and read the rendered file, don't just trust the
  diff of the template source.
- `{{cookiecutter.project_slug}}/CLAUDE.md` ships *inside* every generated
  project and must describe that project's actual selected tools (e.g. only
  the chosen `type_checker`, only the chosen `pre_commit_tool`, omitted
  entirely if `pre_commit_tool == "none"`). It is not the same document as
  this file — do not copy this file's content into it, and do not let the
  generated copy drift back to a static, unconditional file.

## Testing

- Run the suite: `uv run pytest` (uses `pytest-cookies` to bake real
  temporary projects, then asserts on their contents)
- When adding a new cookiecutter variable or choice value, add a
  corresponding `test_*` case that bakes with that option and inspects the
  rendered files — don't just eyeball a manual bake.
- Manually bake a project to `/tmp` for a quick look:
  `uv run cookiecutter . --no-input -o /tmp/bake-out <key>=<value> ...`

## Package management

Same rules as any uv project: `uv add` / `uv add --dev` / `uv remove` /
`uv sync` / `uv lock`. Never edit `[dependency-groups]` here by hand, and
never touch this repo's own `.venv` manually. This applies to the
template-authoring package (`pyproject.toml` at repo root) — it does not
apply to the templated `{{cookiecutter.project_slug}}/pyproject.toml`,
which is Jinja source, not a real manifest.

## What NOT to do

- Do not hand-edit generated output in a baked `/tmp` project and call it
  done — the fix belongs in the template source.
- Do not add a new `cookiecutter.json` choice without updating
  `hooks/post_gen_project.py` (if it needs pruning) and adding bake test
  coverage.
- Do not let `{{cookiecutter.project_slug}}/CLAUDE.md` reference a tool the
  `type_checker` / `pre_commit_tool` choices don't actually offer (e.g. a
  type checker not listed in `cookiecutter.json`).
