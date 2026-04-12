"""Smoke tests — replace with real tests as the project grows."""

from __future__ import annotations


def test_version_is_string() -> None:
    from {{ cookiecutter.package_name }} import __version__

    assert isinstance(__version__, str)
    parts = __version__.split(".")
    assert len(parts) >= 2, "Version should be semver-ish (e.g. 0.1.0)"


def test_importable() -> None:
    """Verify the package can be imported without errors."""
    import {{ cookiecutter.package_name }}  # noqa: F401
    import {{ cookiecutter.package_name }}.dataset  # noqa: F401
    import {{ cookiecutter.package_name }}.features  # noqa: F401
    import {{ cookiecutter.package_name }}.modeling  # noqa: F401
