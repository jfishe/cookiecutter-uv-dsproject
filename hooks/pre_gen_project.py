"""Pre-generation hook — validates template variables before rendering."""

from __future__ import annotations

import re
import sys

SLUG = "{{ cookiecutter.project_slug }}"
PKG = "{{ cookiecutter.package_name }}"

# https://packaging.python.org/en/latest/specifications/name-normalization/
SLUG_RE = re.compile(r"^[a-z][a-z0-9]+(?:[-][a-z0-9]+)*$")
PKG_RE = re.compile(r"^[a-z][a-z0-9_]*$")

RESERVED = {
    "test", "tests", "src", "site", "setup", "pip", "uv",
    "python", "python3", "data", "models", "config", "configs",
}


def _fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not SLUG_RE.match(SLUG):
        _fail(
            f"project_slug '{SLUG}' is invalid. "
            "Use only lowercase letters, digits, and hyphens (must start with a letter)."
        )

    if not PKG_RE.match(PKG):
        _fail(
            f"package_name '{PKG}' is invalid. "
            "Use only lowercase letters, digits, and underscores (must start with a letter)."
        )

    if PKG in RESERVED:
        _fail(f"package_name '{PKG}' collides with a reserved name: {sorted(RESERVED)}")

    if SLUG in RESERVED:
        _fail(f"project_slug '{SLUG}' collides with a reserved name: {sorted(RESERVED)}")


if __name__ == "__main__":
    main()
