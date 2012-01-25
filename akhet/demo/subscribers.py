from akhet.urlgenerator import URLGenerator
import pyramid.threadlocal as threadlocal
from pyramid.exceptions import ConfigurationError

from .lib import helpers

def includeme(config):
    """Configure all application-specific subscribers."""
    config.add_subscriber(create_url_generator, "pyramid.events.ContextFound")
    config.add_subscriber(add_renderer_globals, "pyramid.events.BeforeRender")

def create_url_generator(event):
    """A subscriber for ``pyramid.events.ContextFound`` events.  I create a
    URL generator and attach it to the request (``request.url_generator``).
    Templates and views can then use it to generate application URLs.
    """
    request = event.request
    context = request.context
    url_generator = URLGenerator(context, request, qualified=False)
    request.url_generator = url_generator
    

def add_renderer_globals(event):
    """A subscriber for ``pyramid.events.BeforeRender`` events.  I add
    some :term:`renderer globals` with values that are familiar to Pylons
    users.
    """
    renderer_globals = event
    renderer_globals["h"] = helpers
    request = event.get("request") or threadlocal.get_current_request()
    if not request:
        return
    renderer_globals["r"] = request
    #renderer_globals["c"] = request.tmpl_context
    #try:
    #    renderer_globals["session"] = request.session
    #except ConfigurationError:
    #    pass
    renderer_globals["url"] = request.url_generator


