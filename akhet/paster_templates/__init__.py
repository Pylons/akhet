from paste.deploy.converters import asbool
from paste.script.templates import var
from paste.util.template import paste_script_template_renderer
from pyramid.paster import PyramidTemplate

class AkhetProjectTemplate(PyramidTemplate):
    _template_dir = "akhet"
    summary = "A Pylons-like Pyramid project"
    template_renderer = staticmethod(paste_script_template_renderer)
    vars = [
        var("sqlalchemy", "Include SQLAlchemy configuration? (y/n)",
            default=True),
        ]

    def pre(self, command, output_dir, vars): # pragma: no cover
        """Called before template is applied."""
        PyramidTemplate.pre(self, command, output_dir, vars)
        # Superclass sets vars 'random_string' and 'package_logger'.
        vars["sqlalchemy"] = asbool(vars["sqlalchemy"])
