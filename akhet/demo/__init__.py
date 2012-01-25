from pyramid.config import Configurator
import pyramid_beaker

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Configure Beaker sessions and caching
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    pyramid_beaker.set_cache_regions_from_settings(settings)

    # Configure renderers and event subscribers.
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")
    config.include(".subscribers")
    config.include("akhet.static")

    # Add routes and views.
    config.add_route("home", "/")
    config.include("akhet.pony")
    config.add_static_route("akhet.demo", "static", cache_max_age=3600)
    config.scan()

    return config.make_wsgi_app()


def serve():
    """Run the application like 'pserve development.ini' would do."""

    import logging
    from wsgiref.simple_server import make_server

    fmt = "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
    settings = {
        "pyramid.reload_templates": True,
        "pyramid.debug_authorization": False,
        "pyramid.debug_notfound": False,
        "pyramid.debug_routematch": False,
        "pyramid.debug_templates": True,
        "pyramid.default_locale_name": "en",
        "pyramid.includes": ["pyramid_debugtoolbar"]
        }

    logging.basicConfig(level=logging.INFO, format=fmt)
    logging.getLogger("akhet.demo").setLevel(logging.DEBUG)

    app = main({}, **settings)
    httpd = make_server("127.0.0.1", 5000, app)
    httpd.serve_forever()

if __name__ == "__main__":  serve()
