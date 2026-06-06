"""Smoke tests — replace with real tests as the project grows."""

from __future__ import annotations

from importlib.metadata import version


def test_version_is_string() -> None:
    from {{ cookiecutter.package_name }} import __version__

    assert isinstance(__version__, str)
    assert __version__ == version("{{ cookiecutter.project_slug }}")
    parts = __version__.split(".")
    assert len(parts) >= 2, "Version should be semver-ish (e.g. 0.1.0)"


def test_importable() -> None:
    """Verify the package can be imported without errors."""
    import {{ cookiecutter.package_name }}
    import {{ cookiecutter.package_name }}.dataset
    import {{ cookiecutter.package_name }}.features
    import {{ cookiecutter.package_name }}.modeling  # noqa: F401
