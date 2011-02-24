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

    @reify
    def static(self):
        return url.static_url('baseline:static/', self.request)

    @reify
    def deform(self):
        return url.static_url('deform:static/', self.request)
