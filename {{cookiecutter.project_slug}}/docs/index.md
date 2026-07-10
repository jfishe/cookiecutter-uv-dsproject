# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

```{toctree}
:maxdepth: 2

Overview <readme>
License <license>
{%- if cookiecutter.include_changelog == "yes" %}
Changelog <changelog>
{%- endif %}
apidocs/index
```
