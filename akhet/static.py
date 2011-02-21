import os

import pkg_resources
from pyramid.view import static

def add_static_route(config, package, subdir, cache_max_age=3600,
    **add_route_args):
    """Add a route and view to serve static files from a directory.

    I create a catchall route that serves all URLs from a directory of static
    files if the corresponding file exists. Subdirectories are also handled.
    For example, the URL "/robots.txt" corresponds to file
    "PACKAGE/SUBDIR/robots.txt", and "/images/header/logo.png"
    corresponds to "PACKAGE/SUBDIR/images/header/logo.png".  If the file
    doesn't exist, the route won't match the URL, and Pyramid will continue to
    the next route or traversal. The route name is 'static', which must not
    conflict with your application's other routes.

    Usage in the application's __init__.py::

        from akhet.static import add_static_route
        add_static_route(config, "myapp", "static")

    Or, more conveniently::

        config.include("akhet")
        config.add_static_route("myapp", "static")

    This serves URLs from the "static" directory in package "myapp".

    Arguments:

    * ``config``: a ``pyramid.config.Configurator`` instance.

    * ``package``: the name of the Python package containing the static files.

    * ``subdir``: the subdirectory in the package that contains the files.
      This should be a relative directory with '/' separators regardless of
      platform. 

    * ``cache_max_age``: influences the ``Expires`` and ``Max-Age``
      response headers returned by the view (default is 3600 seconds or five
      minutes).

    * ``**add_route_args``: additional arguments to ``config.add_route``.
      'name' defaults to "static" but can be overridden. (Every route in your
      application must have a unique name.) 'pattern' and 'view' may not be
      specified and will raise TypeError if they are.
    """
    for bad_arg in ["pattern", "view"]:
        if bad_arg in add_route_args:
            raise TypeError("keyword arg '%s' is not allowed")
    name = add_route_args.pop("name", "static")
    pattern = "/*subpath"
    asset = "%s:%s" % (package, subdir)
    view = static(asset, cache_max_age)
    pred = StaticViewPredicate(package, subdir)
    custom_predicates = add_route_args.pop("custom_predicates", [])
    custom_predicates = list(custom_predicates)
    custom_predicates.insert(0, pred)
    config.add_route(name, pattern, view=view, 
        custom_predicates=custom_predicates, **add_route_args)

#### Private stuff

class StaticViewPredicate(object):
    def __init__(self, package, subdir):
        self.package = package
        self.subdir = subdir

    def __call__(self, info, request):
        subpath = info["match"]["subpath"]
        #log.debug("subpath is %r", subpath)
        if not subpath:
            #log.debug("no subpath, returning false")
            return False
        parts = [self.subdir]
        parts.extend(subpath)
        resource_name = "/".join(parts)
        #log.debug("package=%r, resource_name=%r", self.package, resource_name)
        return pkg_resources.resource_exists(self.package, resource_name)
