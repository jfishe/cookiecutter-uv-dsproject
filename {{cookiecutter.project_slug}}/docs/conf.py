"""Sphinx configuration for {{ cookiecutter.project_name }}."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"
copyright = "{% now 'utc', '%Y' %}, {{ cookiecutter.author_name }}"  # noqa: A001

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

autodoc2_packages = ["../src/{{ cookiecutter.package_name }}"]
autodoc2_docstring_parser_regexes = [
    (r".*", "napoleon_numpy_parser"),
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

html_theme = "furo"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}
