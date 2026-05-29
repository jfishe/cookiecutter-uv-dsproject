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
        assert '"mypy>=1.10"' in text
        assert "[tool.mypy]" in text

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

    def test_ty_type_checker_option(self, cookies: Cookies) -> None:
        result = _bake(cookies, type_checker="ty")

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"ty>=0.0.39"' in pyproject
        assert '"joblib>=1.3"' in pyproject
        assert "[tool.ty.environment]" in pyproject
        assert 'python-version = "3.10"' in pyproject
        assert 'include = ["src"]' in pyproject
        assert '"mypy>=1.10"' not in pyproject
        assert "[tool.mypy]" not in pyproject
        assert "pandas-stubs>=2.0" not in pyproject
        assert "joblib-stubs>=1.5.2.0.20250831" not in pyproject

        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "repo: local" in pre_commit
        assert "id: ty" in pre_commit
        assert "uv run ty check src/ --output-format concise --no-progress" in pre_commit
        assert "mirrors-mypy" not in pre_commit

        makefile = (result.project_path / "Makefile").read_text()
        assert "uv run ty check src/" in makefile
        assert "Type-check with ty" in makefile

        workflow = (result.project_path / ".github" / "workflows" / "ci.yml").read_text()
        assert "uv run ty check src/" in workflow
        assert "uv run mypy src/" not in workflow

        readme = (result.project_path / "README.md").read_text()
        assert "ruff, ty, standard hooks" in readme
        assert "Run ty (ensure dev group installed)" in readme


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
        for target in ("install", "fmt", "lint", "test", "docs", "latexpdf", "clean"):
            assert re.search(rf"^{target}:", text, re.MULTILINE)
        assert "IPYTHONDIR=.ipython uv run jupyter lab --notebook-dir=notebooks" in text

    def test_notebook_ux_is_documented(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "nbdime>=4.0" in pyproject
        assert "docrepr>=0.2" in pyproject
        readme = (result.project_path / "README.md").read_text()
        assert "Ctrl+I" in readme
        assert "docrepr" in readme

    def test_docs_starter_files_match_template(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="yes")
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"linkify-it-py>=2.0"' in pyproject
        makefile = (result.project_path / "Makefile").read_text()
        assert "$(MAKE) -C docs html" in makefile
        assert "$(MAKE) -C docs latexpdf" in makefile
        conf = (result.project_path / "docs" / "conf.py").read_text()
        assert '"sphinx.ext.napoleon"' in conf
        assert "napoleon_numpy_docstring = True" in conf
        assert "napoleon_use_param = False" in conf
        assert 'autodoc2_docstring_parser_regexes = [' in conf
        assert 'source_suffix = [".rst", ".md"]' in conf
        assert '"amsmath"' in conf
        assert '"dollarmath"' in conf
        assert '"html_image"' in conf
        assert '"linkify"' in conf
        assert '"replacements"' in conf
        assert '"smartquotes"' in conf
        assert '"substitution"' in conf
        assert "myst_heading_anchors = 5" in conf
        assert 'latex_engine = "xelatex"' in conf
        assert "pdflatex" not in conf
        assert "latex_elements = {}" in conf
        assert "latex_documents = [" in conf
        assert '{{ cookiecutter.project_slug }}.tex' not in conf
        assert "test-project.tex" in conf
        parser_module = (result.project_path / "docs" / "_ext" / "napoleon_numpy_parser.py").read_text()
        assert "class Parser(RstParser):" in parser_module
        assert "NumpyDocstring" in parser_module
        readme = (result.project_path / "README.md").read_text()
        assert "<!-- docs:badges:start -->" in readme
        assert "<!-- docs:badges:end -->" in readme
        docs_readme = (result.project_path / "docs" / "readme.md").read_text()
        assert ":end-before: <!-- docs:badges:start -->" in docs_readme
        assert ":start-after: <!-- docs:badges:end -->" in docs_readme
        docs_makefile = (result.project_path / "docs" / "Makefile").read_text()
        assert "UV_SYNC_DOCS ?= uv sync --group docs" in docs_makefile
        assert "SPHINXBUILD ?= uv run sphinx-build" in docs_makefile
        assert re.search(r"^clean:$", docs_makefile, re.MULTILINE)
        assert '@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"' in docs_makefile
        license_doc = (result.project_path / "docs" / "license.md").read_text()
        assert "../LICENSE" in license_doc
        assert "LICENSE.txt" not in license_doc

        features = (result.project_path / "src" / "test_project" / "features.py").read_text()
        assert "Parameters\n" in features
        assert "Returns\n" in features
        assert ":param df:" not in features

        modeling = (result.project_path / "src" / "test_project" / "modeling.py").read_text()
        assert "Parameters\n" in modeling
        assert "Returns\n" in modeling
        assert ":param model:" not in modeling

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
