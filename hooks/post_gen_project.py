"""Post-generation hook — prunes disabled features, initialises git & uv."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(os.getcwd())

INCLUDE_NOTEBOOKS = "{{ cookiecutter.include_notebooks }}" == "yes"
INCLUDE_DOCS = "{{ cookiecutter.include_docs }}" == "yes"
INCLUDE_DOCKER = "{{ cookiecutter.include_docker }}" == "yes"
INCLUDE_GITHUB_ACTIONS = "{{ cookiecutter.include_github_actions }}" == "yes"


def _remove(rel_path: str) -> None:
    target = PROJECT_DIR / rel_path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.is_file():
        target.unlink()


def prune_features() -> None:
    if not INCLUDE_NOTEBOOKS:
        _remove("notebooks")

    if not INCLUDE_DOCS:
        _remove("docs")

    if not INCLUDE_DOCKER:
        _remove("Dockerfile")

    if not INCLUDE_GITHUB_ACTIONS:
        _remove(".github")


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
    subprocess.run(["uv", "sync", "--all-extras"], cwd=PROJECT_DIR, check=False)


def main() -> None:
    prune_features()
    git_init()
    uv_sync()
    print()
    print(f"✅  Project ready at {PROJECT_DIR}")
    print(f"    cd {PROJECT_DIR.name} && uv run pytest")


if __name__ == "__main__":
    main()
