"""
Contributed by Michael Mericikel.
"""

from pyramid.decorator import reify
import pyramid.url as url

class URLGenerator(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def context(self):
        return url.resource_url(self.context, self.request)

    @reify
    def app(self):
        return self.request.application_url

    def route(self, route_name, *elements, **kw):
        return url.route_url(route_name, self.request, *elements, **kw)

    # sugar for calling url('home')
    __call__ = route

    def current(self, *elements, **kw):
        return url.current_route_url(self.request, *elements, **kw)

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
