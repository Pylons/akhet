::

    class BulkAdder(object):
        def __init__(self, config, route_name):
            self.config = config
            self.route_name = route_name

        def add_view(self, view, **kw):
            config.add_view(view, route_name=self.route_name, **kw)

        def __enter__(self):
            pass

        def __exit__(self, type, value, traceback):
            pass

    def bulk_add_route(config, name, pattern, **kw):
        config.add_route(name, pattern, **kw)
        return BulkAdder(config, name)

    config.add_directive('bulk_add_route', bulk_add_route)

    with config.bulk_add_route('foo', '/foo/{action}') as r:
        r.add_view(foo_view)
        r.add_view(foo_json_view, xhr=True, renderer='json')
        r.add_view(foo_json_post_view, request_method='POST', xhr=True, renderer='json')
