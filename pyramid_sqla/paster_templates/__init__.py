from paste.util.template import paste_script_template_renderer
from pyramid.paster import PyramidTemplate

class PyramidSQLAProjectTemplate(PyramidTemplate):
    _template_dir = "pyramid_sqla"
    summary = "Pyramid SQLAlchemy project with view handlers"
    template_renderer = staticmethod(paste_script_template_renderer)
