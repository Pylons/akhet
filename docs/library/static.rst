Static route
%%%%%%%%%%%%

The static route helper provides a more Pylons-like way to serve static files compared
to Pyramid's standard static view. In Pylons, the static app is an overlay on
"/", so that it looks first for a file under the static directory, and if no
file exists, it falls back to the dynamic application. This static route helper
works the same way: it works as an overlay on "/", so the route matches only if
the file exists, otherwise Pyramid falls through to the next route. The
difference is that Pylons' static app is a WSGI middleware, while the static
route helper registers an ordinary route and a view. By convention you put the static
route last in the route list, but it can go anywhere in the list.

Pyramid's standard `static view`_, in contrast, works only with a URL prefix like
"/static"; it can't serve top-level URLs like "/robots.txt" and "/favicon.ico".
If you want a separate disjunct prefix like "/w3c" (for "/w3c/p3p.xml", the
Internet standard for a machine-readable privacy policy), you'd have to
configure a separate view and static directory for that prefix. With the static route
helper you don't have to configure anything extra, just create a file
"myapp/static/w3c/p3p.xml" and you're done.

The static route helper does have some disadvantages compared to Pyramid's
static view. (1) There's no spiffy method to generate URLs to them. (2) You
can't switch to a static media server and configure the nonexistent spiffy
method to generate external URLs to it.  (3) You can't override assets.

For completeness, we'll mention that if you're using Pyramid's static view,
there are a couple workarounds for serving top-level URLs or disjoint URLs.
(1) Use an ordinary route and view to serve a static file. (2) Use the
"pyramid_assetviews" package on PyPI to serve top-level files. So you can
weigh these alternatives against the static route helper. I (the static route
author) am now undecided, so I can't definitively say which way is better. The
demo app uses it mainly so that you can see it in action.

Usage
=====

::
    
    # In main().
    config.include("akhet.static")
    config.add_static_route("myapp", "static")

API
===

.. function:: config.add_static_route(package, subdir, cache_max_age=3600, \*\*add_route_args)

   Register a route and view to serve any URL if a corresponding file exists
   under the static directory. If the file doesn't exist, the route will fail
   and Pyramid will continue down the route list.

   Arguments:

   * ``package``: the name of the Python package containing the static files.
   * ``subdir``: the subdirectory within the package that contains the files.
     This should be a relative directory with "/" separators regardless of
     platform.
   * ``cache_max_age``: Influences the "Expires" and "Max-Age" HTTP headers in
     the response. (Default is 3600 seconds = 5 minutes.)
   * ``add_route_args``: Additional arguments for ``config.add_route``.
     ``name`` defaults to "static" but can be overridden. (Every route in your
     application must have a unique name.) ``pattern`` and ``view`` may not be
     specified; it will raise TypeError if they are.

The API is from Pyramid's early days, so it makes an asset spec out of
``package`` and ``subdir`` for you and doesn't allow you to supply your own. It
also searches only a single directory rather than a search path. These
limitations may be relaxed in a future version.

Changes in version 2
====================

The include module is now "akhet.static"; in version 1 it was "akhet". A
backward compatibility shim is in place.

.. include:: ../links.rst
