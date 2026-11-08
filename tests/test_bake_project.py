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

    def test_gitignore_ignores_claude_local_settings(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        gitignore = (result.project_path / ".gitignore").read_text()
        assert ".claude/settings.local.json" in gitignore

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
        assert 'requires-python = ">=3.12"' in text
        assert '"mypy>=1.10"' in text
        assert '"prek>=0.5"' in text
        assert '"pre-commit>=3.7"' not in text
        assert "[tool.mypy]" in text
        assert 'lint.pydocstyle.convention = "numpy"' in text
        assert 'convention = "numpy"' in text

        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "id: mypy" in pre_commit
        assert "additional_dependencies: [pandas-stubs, joblib-stubs]" in pre_commit
        assert 'args: ["--config-file=pyproject.toml", "src/"]' in pre_commit
        assert "pass_filenames: false" in pre_commit

    def test_claude_md_matches_default_options(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        claude_md = (result.project_path / ".claude/CLAUDE.md").read_text()
        assert "Tool: mypy" in claude_md
        assert "uv run mypy ." in claude_md
        assert "[tool.mypy]" in claude_md
        assert "Tool: ty" not in claude_md
        assert "uv run ty check" not in claude_md
        assert "[tool.ty]" not in claude_md
        assert "pyrefly" not in claude_md
        assert "Tool: prek, pinned as a dev dependency" in claude_md
        assert "uv run prek install --prepare-hooks -f" in claude_md
        assert "uv run prek run --all-files" in claude_md
        assert "pre-commit" not in claude_md

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
        assert not (result.project_path / "templates").exists()
        makefile = (result.project_path / "Makefile").read_text()
        assert not re.search(r"^jupyter:", makefile, re.MULTILINE)
        readme = (result.project_path / "README.md").read_text()
        assert "- `jupyter`:" not in readme
        assert "templates/latex" not in readme

    def test_no_docs(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="no")
        assert not (result.project_path / "docs").exists()
        assert not (result.project_path / ".readthedocs.yaml").exists()
        makefile = (result.project_path / "Makefile").read_text()
        assert not re.search(r"^docs:", makefile, re.MULTILINE)
        assert not re.search(r"^latexpdf:", makefile, re.MULTILINE)
        readme = (result.project_path / "README.md").read_text()
        assert "- `docs`:" not in readme
        assert "- `latexpdf`:" not in readme

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

    def test_no_changelog(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_changelog="no")
        assert not (result.project_path / "CHANGELOG.md").exists()
        readme = (result.project_path / "README.md").read_text()
        assert "Keep a Changelog + SemVer release notes" not in readme

    def test_default_project_omits_changelog(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        assert not (result.project_path / "CHANGELOG.md").exists()

    def test_pre_commit_tool_none(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="none")
        assert not (result.project_path / ".pre-commit-config.yaml").exists()
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "prek>=" not in pyproject
        assert "pre-commit>=" not in pyproject
        readme = (result.project_path / "README.md").read_text()
        assert "uv run prek install --prepare-hooks -f" not in readme
        assert "uv run pre-commit install --prepare-hooks -f" not in readme
        claude_md = (result.project_path / ".claude/CLAUDE.md").read_text()
        assert "Pre-commit hooks" not in claude_md
        assert "prek" not in claude_md
        assert "pre-commit" not in claude_md

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
        assert "[tool.ty]" in pyproject
        assert 'environment.python-version = "3.12"' in pyproject
        assert 'src.include = [ "src" ]' in pyproject
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

        claude_md = (result.project_path / ".claude/CLAUDE.md").read_text()
        assert "Tool: ty" in claude_md
        assert "uv run ty check" in claude_md
        assert "[tool.ty]" in claude_md
        assert "mypy" not in claude_md
        assert "pyrefly" not in claude_md

    def test_pyrefly_type_checker_option(self, cookies: Cookies) -> None:
        result = _bake(cookies, type_checker="pyrefly")

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"pyrefly>=1.1"' in pyproject
        assert '"joblib>=1.3"' in pyproject
        assert "[tool.pyrefly]" in pyproject
        assert 'python-version = "3.12"' in pyproject
        assert 'project-includes = [ "src" ]' in pyproject
        assert '"mypy>=1.10"' not in pyproject
        assert "[tool.mypy]" not in pyproject
        assert '"ty>=0.0.39"' not in pyproject
        assert "[tool.ty]" not in pyproject
        assert "pandas-stubs>=2" not in pyproject
        assert "joblib-stubs>=1.5.2.0.20250831" not in pyproject

        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "repo: local" in pre_commit
        assert "id: pyrefly" in pre_commit
        assert "uv run pyrefly check --output-format min-text" in pre_commit
        assert "mirrors-mypy" not in pre_commit
        assert "id: ty" not in pre_commit

        makefile = (result.project_path / "Makefile").read_text()
        assert "uv run pyrefly check" in makefile
        assert "Type-check with pyrefly" in makefile

        workflow = (
            result.project_path / ".github" / "workflows" / "ci.yml"
        ).read_text()
        assert "uv run pyrefly check" in workflow
        assert "uv run mypy src/" not in workflow
        assert "uv run ty check src/" not in workflow

        readme = (result.project_path / "README.md").read_text()
        assert "ruff, pyrefly, standard hooks" in readme
        assert "Run pyrefly (ensure dev group installed)" in readme
        assert "uv run prek install --prepare-hooks -f" in readme

        claude_md = (result.project_path / ".claude/CLAUDE.md").read_text()
        assert "Tool: pyrefly" in claude_md
        assert "uv run pyrefly check" in claude_md
        assert "[tool.pyrefly]" in claude_md
        assert "Tool: mypy" not in claude_md
        assert "Tool: ty" not in claude_md

    def test_pre_commit_runner_option(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="pre-commit")

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert '"pre-commit>=3.7"' in pyproject
        assert '"prek>=0.5"' not in pyproject

        pre_commit = result.project_path / ".pre-commit-config.yaml"
        assert pre_commit.is_file()

        readme = (result.project_path / "README.md").read_text()
        assert "uv run pre-commit install --prepare-hooks -f" in readme
        assert "uv run pre-commit run --all-files" in readme
        assert "uv run prek install --prepare-hooks -f" not in readme

        claude_md = (result.project_path / ".claude/CLAUDE.md").read_text()
        assert "Tool: pre-commit, pinned as a dev dependency" in claude_md
        assert "uv run pre-commit install --prepare-hooks -f" in claude_md
        assert "uv run prek install" not in claude_md

    def test_prek_uses_builtin_hooks(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="prek")
        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "repo: builtin" in pre_commit
        assert "uv run prek update --cooldown-days 7" in pre_commit
        # Hooks with no prek builtin still come from pre-commit-hooks.
        hooks_repo = pre_commit.split("pre-commit/pre-commit-hooks", 1)[1]
        hooks_repo = hooks_repo.split("- repo:", 1)[0]
        assert "id: check-ast" in hooks_repo
        assert "id: trailing-whitespace" not in hooks_repo

    def test_pre_commit_runner_has_no_builtin_hooks(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="pre-commit")
        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "repo: builtin" not in pre_commit
        assert "id: trailing-whitespace" in pre_commit
        assert "uv run pre-commit autoupdate" in pre_commit

    def test_markdown_hooks_use_rumdl(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        pre_commit = (result.project_path / ".pre-commit-config.yaml").read_text()
        assert "id: rumdl-check" in pre_commit
        assert "id: ruff-check" in pre_commit
        assert "types_or: [python, pyi, jupyter, markdown]" in pre_commit
        assert "markdownlint" not in pre_commit
        assert "mdformat" not in pre_commit

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "[tool.rumdl]" in pyproject
        assert '"ruff>=0.16"' in pyproject
        assert 'per-file-flavor."docs/**/*.md" = "myst"' in pyproject

    def test_rumdl_config_omitted_without_hooks(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="none")
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "[tool.rumdl]" not in pyproject

    def test_rumdl_myst_flavor_omitted_without_docs(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="no")
        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert "[tool.rumdl]" in pyproject
        assert "per-file-flavor" not in pyproject

    def test_workflow_linters_follow_github_actions_option(
        self, cookies: Cookies
    ) -> None:
        with_gha = _bake(cookies, include_github_actions="yes")
        pre_commit = (with_gha.project_path / ".pre-commit-config.yaml").read_text()
        assert "id: actionlint" in pre_commit
        assert "id: zizmor" in pre_commit

        without_gha = _bake(cookies, include_github_actions="no")
        pre_commit = (without_gha.project_path / ".pre-commit-config.yaml").read_text()
        assert "actionlint" not in pre_commit
        assert "zizmor" not in pre_commit

    def test_ci_lint_job_runs_hook_runner(self, cookies: Cookies) -> None:
        for tool in ("prek", "pre-commit"):
            result = _bake(cookies, pre_commit_tool=tool)
            workflow = (
                result.project_path / ".github" / "workflows" / "ci.yml"
            ).read_text()
            assert f"uv run {tool} run --all-files --show-diff-on-failure" in workflow
            assert "uv run ruff check src/ tests/" not in workflow

        result = _bake(cookies, pre_commit_tool="none")
        workflow = (
            result.project_path / ".github" / "workflows" / "ci.yml"
        ).read_text()
        assert "uv run ruff check src/ tests/" in workflow

    def test_dependabot_tracks_uv_and_hooks(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        dependabot = (result.project_path / ".github" / "dependabot.yml").read_text()
        assert "package-ecosystem: uv" in dependabot
        assert "package-ecosystem: pip" not in dependabot
        assert "package-ecosystem: pre-commit" in dependabot

        result = _bake(cookies, pre_commit_tool="none")
        dependabot = (result.project_path / ".github" / "dependabot.yml").read_text()
        assert "package-ecosystem: pre-commit" not in dependabot

    def test_ci_matrix_has_no_duplicate_python(self, cookies: Cookies) -> None:
        same = _bake(cookies, python_version="3.12", min_python_version="3.12")
        workflow = (same.project_path / ".github" / "workflows" / "ci.yml").read_text()
        assert workflow.count('- "3.12"') == 1

        spread = _bake(cookies, python_version="3.14", min_python_version="3.12")
        workflow = (
            spread.project_path / ".github" / "workflows" / "ci.yml"
        ).read_text()
        assert '- "3.12"' in workflow
        assert '- "3.14"' in workflow


# ---------------------------------------------------------------------------
# Content checks
# ---------------------------------------------------------------------------


class TestContent:
    def test_version_in_init(self, cookies: Cookies) -> None:
        result = _bake(cookies, initial_version="1.2.3")
        init = (
            result.project_path / "src" / "test_project" / "__init__.py"
        ).read_text()
        assert "from importlib.metadata import PackageNotFoundError, version" in init
        assert '__version__ = version("test-project")' in init
        assert "except PackageNotFoundError:" in init
        assert '__version__ = "0.0.0"' in init
        assert '"1.2.3"' not in init

    def test_changelog_scaffold_uses_keepachangelog_and_semver(
        self, cookies: Cookies
    ) -> None:
        result = _bake(cookies, include_changelog="yes", initial_version="1.2.3")
        changelog = (result.project_path / "CHANGELOG.md").read_text()
        assert "https://keepachangelog.com/en/1.1.0/" in changelog
        assert "https://semver.org/spec/v2.0.0.html" in changelog
        assert "## [v1.2.3]" in changelog
        assert (
            "[unreleased]: https://github.com/testuser/test-project/compare/"
            "v1.2.3...HEAD"
        ) in changelog
        assert (
            "[v1.2.3]: https://github.com/testuser/test-project/releases/tag/v1.2.3"
        ) in changelog

    def test_license_mit(self, cookies: Cookies) -> None:
        result = _bake(cookies, license="MIT")
        text = (result.project_path / "LICENSE").read_text()
        assert "MIT" in text

    def test_makefile_has_targets(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        text = (result.project_path / "Makefile").read_text()
        for target in (
            "install",
            "fmt",
            "lint",
            "test",
            "audit",
            "jupyter",
            "docs",
            "latexpdf",
            "clean",
        ):
            assert re.search(rf"^{target}:", text, re.MULTILINE)
        assert re.search(r"^docker-build:", text, re.MULTILINE)
        assert "UV_PROJECT_PYTHON ?= 3.12" in text
        assert "UV_SYNC ?= uv sync --python $(UV_PROJECT_PYTHON)" in text
        assert "uv python install $(UV_PROJECT_PYTHON)" in text
        assert "$(UV_SYNC) --all-groups" in text
        assert "IPYTHONDIR=.ipython uv run jupyter lab --notebook-dir=notebooks" in text
        assert "$(UV_SYNC) --group notebooks" in text
        assert "$(UV_SYNC) --group notebooks || true" not in text

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

    def test_pre_commit_runner_hooks_pass(self, cookies: Cookies) -> None:
        result = _bake(cookies, pre_commit_tool="pre-commit")
        completed = subprocess.run(
            ["uv", "run", "pre-commit", "run", "--all-files"],
            cwd=result.project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr

    def test_default_project_make_audit_passes(self, cookies: Cookies) -> None:
        result = _bake(cookies)
        readme = (result.project_path / "README.md").read_text()
        assert "- `audit`:" in readme

        completed = subprocess.run(
            ["make", "audit"],
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
        assert docs_readme.startswith("# Overview\n")
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

    def test_docs_build_without_sphinx_warnings(self, cookies: Cookies) -> None:
        result = _bake(cookies, include_docs="yes")
        sync = subprocess.run(
            ["uv", "sync", "--group", "docs"],
            cwd=result.project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert sync.returncode == 0, sync.stdout + sync.stderr

        completed = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-W",
                "-b",
                "html",
                "docs",
                "docs/_build/html",
            ],
            cwd=result.project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr

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
