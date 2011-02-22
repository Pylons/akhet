from akhet.static import add_static_route

def includeme(config):
    """Add certain useful methods to a Pyramid ``Configurator`` instance.

    Currently this adds the ``.add_static_route()`` method. (See
    ``pyramid_sqla.static.add_static_route()``.)
    """
    config.add_directive('add_static_route', add_static_route)
