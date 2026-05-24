"""Tests for baking the cookiecutter template."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bake(cookies: Cookies, **overrides: str) -> Result:
    defaults = {
        "project_name": "Test Project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "github_username": "testuser",
    }
    defaults.update(overrides)
    return cookies.bake(extra_context=defaults)


# ---------------------------------------------------------------------------
# Structure & basics
# ---------------------------------------------------------------------------

class TestBasicBake:
    def test_bake_exits_zero(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        assert result.exit_code == 0, result.exception

    def test_project_slug(self, cookies: Cookies) -> None:
        result = _bake(cookies, project_name="My Cool Project")
        assert result.project_path.name == "my-cool-project"

    def test_src_layout(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        pkg = result.project_path / "src" / "test_project"
        assert pkg.is_dir()
        assert (pkg / "__init__.py").is_file()
        assert (pkg / "dataset.py").is_file()
        assert (pkg / "features.py").is_file()
        assert (pkg / "modeling.py").is_file()

    def test_ds_directories_exist(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        for subdir in ("raw", "interim", "processed", "external"):
            assert (result.project_path / "data" / subdir).is_dir()
        assert (result.project_path / "models").is_dir()
        assert (result.project_path / "reports" / "figures").is_dir()
        assert (result.project_path / "configs").is_dir()

    def test_pyproject_toml_valid(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        text = (result.project_path / "pyproject.toml").read_text()
        assert 'name = "test-project"' in text
        assert 'requires-python = ">=3.10"' in text

    def test_starter_notebook_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        nb = result.project_path / "notebooks" / "getting-started.ipynb"
        assert nb.is_file()
        # Verify it's parseable JSON with the right structure
        data = json.loads(nb.read_text())
        assert data["nbformat"] == 4
        assert len(data["cells"]) >= 5

    def test_notebook_inspector_config_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        config = result.project_path / ".ipython" / "profile_default" / "ipython_config.py"
        assert config.is_file()
        text = config.read_text()
        assert "InteractiveShell.sphinxify_docstring = True" in text
        assert "InteractiveShell.enable_html_pager = True" in text

    def test_train_script_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        script = result.project_path / "scripts" / "train_model.py"
        assert script.is_file()
        text = script.read_text()
        assert "argparse" in text
        assert "test_project" in text  # package_name for "Test Project"


# ---------------------------------------------------------------------------
# Feature toggles
# ---------------------------------------------------------------------------

class TestFeatureToggles:
    def test_no_notebooks(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_notebooks="no")
        assert not (result.project_path / "notebooks").exists()
        assert not (result.project_path / ".ipython").exists()

    def test_no_docs(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="no")
        assert not (result.project_path / "docs").exists()

    def test_no_docker(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docker="no")
        assert not (result.project_path / "Dockerfile").exists()

    def test_no_github_actions(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_github_actions="no")
        assert not (result.project_path / ".github").exists()

    def test_no_notebooks_removes_ipynb(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_notebooks="no")
        assert not (result.project_path / "notebooks" / "getting-started.ipynb").exists()

    def test_notebook_ux_can_be_disabled(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_notebook_ux="no")
        assert not (result.project_path / ".ipython").exists()
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "docrepr>=0.2" not in pyproject
        makefile = (result.project_path / "Makefile").read_text()
        assert "IPYTHONDIR=.ipython" not in makefile
        readme = (result.project_path / "README.md").read_text()
        assert "rich inspector help" not in readme


# ---------------------------------------------------------------------------
# Content checks
# ---------------------------------------------------------------------------

class TestContent:
    def test_version_in_init(self, cookies: Cookies) -> None:
        result = _bake(cookies, initial_version="1.2.3")
        init = (result.project_path / "src" / "test_project" / "__init__.py").read_text()
        assert '"1.2.3"' in init

    def test_license_mit(self, cookies: Cookies) -> None:
        result = _bake(cookies, license="MIT")
        text = (result.project_path / "LICENSE").read_text()
        assert "MIT" in text

    def test_makefile_has_targets(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        text = (result.project_path / "Makefile").read_text()
        for target in ("install", "fmt", "lint", "test", "clean"):
            assert re.search(rf"^{target}:", text, re.MULTILINE)
        assert "IPYTHONDIR=.ipython uv run jupyter lab --notebook-dir=notebooks" in text

    def test_notebook_ux_is_documented(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "docrepr>=0.2" in pyproject
        readme = (result.project_path / "README.md").read_text()
        assert "Ctrl+I" in readme
        assert "docrepr" in readme

    def test_ci_workflow_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        assert (result.project_path / ".github" / "workflows" / "ci.yml").is_file()


# ---------------------------------------------------------------------------
# Validation hooks
# ---------------------------------------------------------------------------

class TestValidation:
    def test_invalid_slug_fails(self, cookies: Cookies) -> None:
        result = _bake(cookies, project_slug="123-bad")
        assert result.exit_code != 0
