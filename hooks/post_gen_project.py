"""Post-generation hook — prunes disabled features, initialises git & uv."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(os.getcwd())

INCLUDE_NOTEBOOKS = "{{ cookiecutter.include_notebooks }}" == "yes"
INCLUDE_NOTEBOOK_UX = "{{ cookiecutter.include_notebook_ux }}" == "yes"
INCLUDE_DOCS = "{{ cookiecutter.include_docs }}" == "yes"
INCLUDE_DOCKER = "{{ cookiecutter.include_docker }}" == "yes"
INCLUDE_GITHUB_ACTIONS = "{{ cookiecutter.include_github_actions }}" == "yes"
INCLUDE_CHANGELOG = "{{ cookiecutter.include_changelog }}" == "yes"
PRE_COMMIT_TOOL = "{{ cookiecutter.pre_commit_tool }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"


def _remove(rel_path: str) -> None:
    target = PROJECT_DIR / rel_path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.is_file():
        target.unlink()


def prune_features() -> None:
    if not INCLUDE_NOTEBOOKS:
        _remove("notebooks")
        _remove(".ipython")
    elif not INCLUDE_NOTEBOOK_UX:
        _remove(".ipython")

    if not INCLUDE_DOCS:
        _remove("docs")
        _remove(".readthedocs.yaml")

    if not INCLUDE_DOCKER:
        _remove("Dockerfile")

    if not INCLUDE_GITHUB_ACTIONS:
        _remove(".github")

    if not INCLUDE_CHANGELOG:
        _remove("CHANGELOG.md")

    if PRE_COMMIT_TOOL == "none":
        _remove(".pre-commit-config.yaml")


def git_init() -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=PROJECT_DIR, check=False)
    subprocess.run(["git", "add", "."], cwd=PROJECT_DIR, check=False)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit (cookiecutter-uv-dsproject)"],
        cwd=PROJECT_DIR,
        check=False,
    )


def uv_sync() -> None:
    if shutil.which("uv") is None:
        print("⚠  uv not found on PATH — skipping lock & sync.", file=sys.stderr)
        print("   Install uv: https://docs.astral.sh/uv/getting-started/installation/")
        return
    subprocess.run(
        ["uv", "python", "install", PYTHON_VERSION], cwd=PROJECT_DIR, check=False
    )
    subprocess.run(
        ["uv", "sync", "--all-extras", "--python", PYTHON_VERSION],
        cwd=PROJECT_DIR,
        check=False,
    )


def main() -> None:
    prune_features()
    git_init()
    uv_sync()
    print()
    print(f"✅  Project ready at {PROJECT_DIR}")
    print(f"    cd {PROJECT_DIR.name} && uv run pytest")


if __name__ == "__main__":
    main()
