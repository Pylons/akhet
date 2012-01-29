import unittest

import pyramid.static

import akhet
import akhet.static

class TestAddStaticRoute(unittest.TestCase):
    def _callFUT(self, config, package, subdir, cache_max_age=3600,
                 **add_route_args):
        return akhet.static.add_static_route(config, package, subdir,
                                cache_max_age=cache_max_age, **add_route_args)

    def test_pattern_is_bad_arg(self):
        self.assertRaises(TypeError, self._callFUT,
                          None, None, None, pattern="foo")

    def test_view_is_bad_arg(self):
        self.assertRaises(TypeError, self._callFUT,
                          None, None, None, view="foo")

    def test_has_name(self):
        config = DummyConfig()
        self._callFUT(config, "package", "subdir", name="myname")
        self.assertEqual(len(config.routes), 1)
        route = config.routes[0]
        self.assertEqual(route["pattern"], "/*subpath")
        self.assertEqual(route["name"], "myname")
        self.assertEqual(route["kw"]["custom_predicates"][0].__class__,
            akhet.static.StaticViewPredicate)
        self.assertEqual(config.views["myname"].__class__,
            pyramid.static.static_view)

    def test_has_no_name(self):
        config = DummyConfig()
        self._callFUT(config, "package", "subdir")
        self.assertEqual(len(config.routes), 1)
        route = config.routes[0]
        self.assertEqual(route["pattern"], "/*subpath")
        self.assertEqual(route["name"], "static")

class TestStaticViewPredicate(unittest.TestCase):
    def _makeOne(self, package, subdir):
        return akhet.static.StaticViewPredicate(package, subdir)

    def test___call___has_no_subpath(self):
        inst = self._makeOne("package", "subdir")
        self.assertEqual(inst({"match":{"subpath":()}}, None), False)

    def test___call___resource_exists(self):
        inst = self._makeOne("akhet", "tests")
        self.assertEqual(
            inst({"match":{"subpath":("test_static.py",)}}, None), True)

    def test___call___resource_doesnt_exist(self):
        inst = self._makeOne("akhet", "tests")
        self.assertEqual(inst({"match":{"subpath":("wont.py",)}}, None), False)


class DummyConfig(object):
    def __init__(self):
        self.routes = []
        self.views = {}   # ``{route_name: view}``
        self.directives = {}

    def add_route(self, name, pattern, **kw):
        self.routes.append({"name":name, "pattern":pattern, "kw":kw})

    def add_view(self, view, **kw):
        route_name = kw.get("route_name")
        if route_name:
            self.views[route_name] = view

