"""Sphinx configuration for {{ cookiecutter.project_name }}."""

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"
copyright = "{% now 'utc', '%Y' %}, {{ cookiecutter.author_name }}"  # noqa: A001

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

autodoc2_packages = ["../src/{{ cookiecutter.package_name }}"]

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
