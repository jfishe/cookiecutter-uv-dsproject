"""Tests for baking the cookiecutter template."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

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
        assert '"prek>=0.4.3"' in text
        assert '"pre-commit>=3.7"' not in text
        assert "[tool.mypy]" in text
        assert 'lint.pydocstyle.convention = "numpy"' in text
        assert 'convention = "numpy"' in text

        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "id: mypy" in pre_commit
        assert "additional_dependencies: [pandas-stubs, joblib-stubs]" in pre_commit
        assert 'args: ["--config-file=pyproject.toml", "src/"]' in pre_commit
        assert "pass_filenames: false" in pre_commit

    def test_starter_notebook_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        nb = result.project_path / "notebooks" / "getting-started.ipynb"
        assert nb.is_file()
        # Verify it's parseable JSON with the right structure
        data = json.loads(nb.read_text())
        assert data["nbformat"] == 4
        assert len(data["cells"]) >= 5
        assert data["metadata"]["title"] == "Test Project getting started"
        assert data["metadata"]["latex_export"] == {
            "document_id": "DOC-0001",
            "page_prefix": "A-",
            "revision": "0",
        }
        notebook_source = "\n".join("".join(cell["source"]) for cell in data["cells"])
        assert (
            "from test_project.display import configure_notebook_display, display_dataframe"
            in notebook_source
        )
        assert "configure_notebook_display()" in notebook_source
        assert 'caption="Example notebook summary"' in notebook_source
        assert r"\autoref{tab:example-notebook-summary}" in notebook_source
        table_cells = [
            cell
            for cell in data["cells"]
            if cell.get("metadata", {}).get("table_export")
        ]
        assert len(table_cells) == 1
        table_export = table_cells[0]["metadata"]["table_export"]
        assert table_export["title"] == "Example notebook summary"
        assert table_export["caption"] == "Example notebook summary"
        assert table_export["label"] == "tab:example-notebook-summary"
        latex_template = result.project_path / "templates" / "latex" / "index.tex.j2"
        assert latex_template.is_file()
        latex_conf = result.project_path / "templates" / "latex" / "conf.json"
        assert latex_conf.is_file()
        template_text = latex_template.read_text()
        assert "nb.metadata.get('latex_export', {})" in template_text
        assert r"\usepackage{fancyhdr}" in template_text
        assert r"\fancyhead[R]{\notebookheadertext}" in template_text
        assert r"\renewcommand{\thepage}" in template_text
        assert (
            r"\captionsetup[table]{format=plain, font=small, labelfont=bf, labelsep=colon}"
            in template_text
        )
        assert (
            r"\captionsetup[longtable]{format=plain, font=small, labelfont=bf, labelsep=colon}"
            in template_text
        )
        assert '"base_template": "latex"' in latex_conf.read_text()

    def test_notebook_inspector_config_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        config = (
            result.project_path / ".ipython" / "profile_default" / "ipython_config.py"
        )
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
        assert not (result.project_path / ".readthedocs.yaml").exists()

    def test_no_docker(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docker="no")
        assert not (result.project_path / "Dockerfile").exists()
        makefile = (result.project_path / "Makefile").read_text()
        assert not re.search(r"^docker-build:", makefile, re.MULTILINE)
        readme = (result.project_path / "README.md").read_text()
        assert "Dockerfile" not in readme

    def test_no_github_actions(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_github_actions="no")
        assert not (result.project_path / ".github").exists()

    def test_pre_commit_tool_none(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="none")
        assert not (result.project_path / ".pre-commit-config.yaml").exists()
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "prek>=" not in pyproject
        assert "pre-commit>=" not in pyproject
        readme = (result.project_path / "README.md").read_text()
        assert "uv run prek install --prepare-hooks -f" not in readme
        assert "uv run pre-commit install --prepare-hooks -f" not in readme

    def test_no_notebooks_removes_ipynb(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_notebooks="no")
        assert not (
            result.project_path / "notebooks" / "getting-started.ipynb"
        ).exists()

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
        assert 'include = [ "src" ]' in pyproject
        assert '"mypy>=1.10"' not in pyproject
        assert "[tool.mypy]" not in pyproject
        assert "pandas-stubs>=2" not in pyproject
        assert "joblib-stubs>=1.5.2.0.20250831" not in pyproject

        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "repo: local" in pre_commit
        assert "id: ty" in pre_commit
        assert (
            "uv run ty check src/ --output-format concise --no-progress" in pre_commit
        )
        assert "mirrors-mypy" not in pre_commit

        makefile = (result.project_path / "Makefile").read_text()
        assert "uv run ty check src/" in makefile
        assert "Type-check with ty" in makefile

        workflow = (
            result.project_path / ".github" / "workflows" / "ci.yml"
        ).read_text()
        assert "uv run ty check src/" in workflow
        assert "uv run mypy src/" not in workflow

        readme = (result.project_path / "README.md").read_text()
        assert "ruff, ty, standard hooks" in readme
        assert "Run ty (ensure dev group installed)" in readme
        assert "uv run prek install --prepare-hooks -f" in readme

    def test_pre_commit_runner_option(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="pre-commit")

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"pre-commit>=3.7"' in pyproject
        assert '"prek>=0.4.3"' not in pyproject

        pre_commit = result.project_path / ".pre-commit-config.yaml"
        assert pre_commit.is_file()

        readme = (result.project_path / "README.md").read_text()
        assert "uv run pre-commit install --prepare-hooks -f" in readme
        assert "uv run pre-commit run --all-files" in readme
        assert "uv run prek install --prepare-hooks -f" not in readme


# ---------------------------------------------------------------------------
# Content checks
# ---------------------------------------------------------------------------


class TestContent:
    def test_version_in_init(self, cookies: Cookies) -> None:
        result = _bake(cookies, initial_version="1.2.3")
        init = (
            result.project_path / "src" / "test_project" / "__init__.py"
        ).read_text()
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
        assert re.search(r"^docker-build:", text, re.MULTILINE)
        assert "UV_PROJECT_PYTHON ?= 3.12" in text
        assert "UV_SYNC ?= uv sync --python $(UV_PROJECT_PYTHON)" in text
        assert "uv python install $(UV_PROJECT_PYTHON)" in text
        assert "$(UV_SYNC) --all-groups" in text
        assert "IPYTHONDIR=.ipython uv run jupyter lab --notebook-dir=notebooks" in text

    def test_post_gen_hook_uses_selected_python(self, cookies: Cookies) -> None:
        _bake(cookies)
        hook = (
            Path(__file__).resolve().parents[1] / "hooks" / "post_gen_project.py"
        ).read_text()
        assert 'PYTHON_VERSION = "{{ cookiecutter.python_version }}"' in hook
        assert '["uv", "python", "install", PYTHON_VERSION]' in hook
        assert '["uv", "sync", "--all-extras", "--python", PYTHON_VERSION]' in hook

    def test_notebook_ux_is_documented(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "nbdime>=4" in pyproject
        assert "jinja2>=3.1" in pyproject
        assert "docrepr>=0.2" in pyproject
        readme = (result.project_path / "README.md").read_text()
        assert "Ctrl+I" in readme
        assert "docrepr" in readme
        assert "display_dataframe" in readme
        assert "nbconvert --to pdf" in readme
        assert "--template=templates/latex" in readme
        assert "metadata.latex_export" in readme

    def test_dataframe_display_helper_exists(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        helper = (
            result.project_path / "src" / "test_project" / "display.py"
        ).read_text()
        assert "def configure_notebook_display" in helper
        assert "def display_dataframe" in helper
        assert 'msg = "label requires a caption"' in helper
        assert '"text/latex": styler.to_latex(' in helper
        assert 'find_spec("jinja2") is None' in helper

    def test_default_project_mypy_typechecks(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        completed = subprocess.run(
            ["uv", "run", "mypy", "src/"],
            cwd=result.project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr

    def test_default_project_prek_hooks_pass(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        completed = subprocess.run(
            ["uv", "run", "prek", "run", "--all-files"],
            cwd=result.project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr

    def test_docs_starter_files_match_template(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="yes")
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"linkify-it-py>=2"' in pyproject
        makefile = (result.project_path / "Makefile").read_text()
        assert "$(MAKE) -C docs html" in makefile
        assert "$(MAKE) -C docs latexpdf" in makefile
        conf = (result.project_path / "docs" / "conf.py").read_text()
        assert '"sphinx.ext.napoleon"' in conf
        assert "napoleon_numpy_docstring = True" in conf
        assert "napoleon_use_param = False" in conf
        assert "autodoc2_docstring_parser_regexes = [" in conf
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
        assert "{{ cookiecutter.project_slug }}.tex" not in conf
        assert "test-project.tex" in conf
        parser_module = (
            result.project_path / "docs" / "_ext" / "napoleon_numpy_parser.py"
        ).read_text()
        assert "class Parser(RstParser):" in parser_module
        assert "NumpyDocstring" in parser_module
        readme = (result.project_path / "README.md").read_text()
        assert "<!-- docs:badges:start -->" in readme
        assert "<!-- docs:badges:end -->" in readme
        docs_readme = (result.project_path / "docs" / "readme.md").read_text()
        assert "<!-- markdownlint-disable-file MD041 -->" in docs_readme
        assert ":end-before: <!-- docs:badges:start -->" in docs_readme
        assert ":start-after: <!-- docs:badges:end -->" in docs_readme
        docs_makefile = (result.project_path / "docs" / "Makefile").read_text()
        assert "UV_PROJECT_PYTHON ?= 3.12" in docs_makefile
        assert (
            "UV_SYNC_DOCS ?= uv sync --python $(UV_PROJECT_PYTHON) --group docs"
            in docs_makefile
        )
        assert "SPHINXBUILD ?= uv run sphinx-build" in docs_makefile
        assert re.search(r"^clean:$", docs_makefile, re.MULTILINE)
        assert '@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"' in docs_makefile
        rtd_config = (result.project_path / ".readthedocs.yaml").read_text()
        assert "version: 2" in rtd_config
        assert "os: ubuntu-24.04" in rtd_config
        assert 'python: "3.12"' in rtd_config
        assert "configuration: docs/conf.py" in rtd_config
        assert "method: uv" in rtd_config
        assert "command: sync" in rtd_config
        assert "groups:" in rtd_config
        assert "- docs" in rtd_config
        license_doc = (result.project_path / "docs" / "license.md").read_text()
        assert "../LICENSE" in license_doc
        assert "LICENSE.txt" not in license_doc

        features = (
            result.project_path / "src" / "test_project" / "features.py"
        ).read_text()
        assert "Parameters\n" in features
        assert "Returns\n" in features
        assert ":param df:" not in features

        modeling = (
            result.project_path / "src" / "test_project" / "modeling.py"
        ).read_text()
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
