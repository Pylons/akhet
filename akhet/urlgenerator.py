"""Convenience methods for generating URLs in templates.

I shadow various URL-generating functions in ``pyramid.url`` and attributes in
the request. My main use is in templates where my method names are shorter than
the originals and you don't have to pass a request argument. In Akhet, a
subscriber callback registers an instance of me as ``request.url_generator``,
and another callback aliases me to the ``url`` global in templates. These
callbacks are defined in *myapp/subscribers.py*.

The source code contains commented examples of "static_url" methods. We're not
sure what's best here so we're leaving them commented and you can define them in
a subclass however you wish. That's better than releasing a bad API which we'll
then have to change and break existing apps.

Contributed by Michael Merickel. Modified by Mike Orr.
"""

from pyramid.decorator import reify
import pyramid.url as url

class URLGenerator(object):
    def __init__(self, context, request, qualified=False):
        """Instantiate a URLGenerator based on the current request.
        
        * ``request``: a Pyramid Request.
        * ``context``: a Pyramid Context.
        * ``qualified``: If true, return fully-qualified URLs
          with the "scheme://host" prefix. If false (default), return only the
          URL path if the underlying Pyramid function allows it.
        """
        self.context = context
        self.request = request
        self.qualified = qualified

    @reify
    def ctx(self):
        """The URL of the default view for the current context.

        I'm a "reified" attribute which means I start out as a property but
        I turn into an ordinary string attribute on the first access.
        This saves CPU cycles if I'm accessed often.

        I am mainly used with traversal. I am different from ``.app`` when
        using context factories. I always return a qualified URL regardless
        of the constructor's 'qualified' argument.
        """
        return url.resource_url(self.context, self.request)

    @reify
    def app(self):
        """The application URL or path.

        I'm a "reified" attribute which means I start out as a property but
        I turn into an ordinary string attribute on the first access.
        This saves CPU cycles if I'm accessed often.

        I return the application prefix of the URL. Append a slash to get the
        home page URL, or additional path segments to get a sub-URL.

        If the constructor arg 'qualified' is true, I return
        ``request.application_url``, otherwise I return ``request.script_name``.
        """
        if self.qualified:
            return self.request.application_url
        else:
            return self.request.script_name

    def route(self, route_name, *elements, **kw):
        """Generate a route URL.

        I return a URL based on a named route. Calling the URLGenerator 
        instance is the same as calling me.
        If the constructor arg 'qualified' is true, I call
        ``pyramid.url.route_url``, otherwise I call ``pyramid.url.route_path``.

        Arguments: 

        * ``route_name``: the name of a route.
        * ``*elements``: additional segments to append to the URL path.


        Keyword arguments are passed to the underlying function. The following
        are recognized:

        * ``_query``: the query parameters. May be a dict-like object with
          an ``.items()`` method or a sequence of 2-tuples.
        * ``_anchor``: the URL's "#ancor" fragment without the "#".
        * ``_qualified``: override the constructor's "qualified" flag.
        * ``_app_url``: override the "scheme://host" prefix. (This also causes
          the result to be qualified if it wouldn't otherwise be.)
        * Other keyword args override path variables defined in the route.

        If the relevant route has a *pregenerator* defined, it may modify the
        elements or keyword args.
        """
        qualified = kw.get("_qualified", self.qualified)
        if qualified or "_app_url" in kw:
            return url.route_url(route_name, self.request, *elements, **kw)
        else:
            return url.route_path(route_name, self.request, *elements, **kw)

    # sugar for calling url('home')
    __call__ = route

    def current(self, *elements, **kw):
        """Generate a URL based on the current request's route.

        I call ``pyramid.url.current_route_url``. I'm the same as calling
        ``.route`` with the current route name. The result is always qualified
        regardless of the constructor's 'qualified' argument.
        """
        return url.current_route_url(self.request, *elements, **kw)

    def resource(self, *elements, **kw):
        """Return a "resource URL" as used in traversal.

        ``*elements`` is the same as with ``.route``. Keyword args ``query``
        and ``anchor`` are the same as the ``_query`` and ``_anchor`` args to
        ``.route``.

        When called without arguments, I return the same as ``.ctx``.
        """
        return url.resource_url(self.context, self.request, *elements, **kw)

    ## Commented because I'm unsure of the long-term API.
    ## If you want to use this, or a more particular one for your
    ## static package(s), define it in a subclass.
    ##
    #  A future version might make 'path' optional, defaulting to
    #  a value passed to the constructor ("myapp:static/").
    #
    #def static(self, path, **kw):
    #    return url.static_url(path, self.request, **kw)
    

    ## If you're using the Deform package you may find this useful.
    #
    #@reify
    #def deform(self):
    #    return url.static_url("deform:static/", self.request)
