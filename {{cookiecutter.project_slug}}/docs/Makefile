# Minimal Sphinx makefile for generated projects.

UV_PROJECT_PYTHON ?= {{ cookiecutter.python_version }}
UV_SYNC_DOCS ?= uv sync --python $(UV_PROJECT_PYTHON) --group docs
SPHINXBUILD ?= uv run sphinx-build
SPHINXOPTS ?=
SOURCEDIR = .
BUILDDIR = _build

.PHONY: help clean Makefile

help:
	@$(UV_SYNC_DOCS)
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf "$(BUILDDIR)"

%: Makefile
	@$(UV_SYNC_DOCS)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
