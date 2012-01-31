import unittest

from akhet import urlgenerator

from pyramid import testing

class TestURLGenerator(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        
    def _makeOne(self, context, request, qualified=False):
        return urlgenerator.URLGenerator(context, request, qualified=qualified)

    def test_ctor(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        self.assertEqual(inst.context, context)
        self.assertEqual(inst.request, request)
        self.assertEqual(inst.qualified, True)
        
    def test_ctx(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst.ctx
        self.assertEqual(result, 'http://example.com/')

    def test_app_qualified(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst.app
        self.assertEqual(result, 'http://example.com')

    def test_app_notqualified(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, False)
        result = inst.app
        self.assertEqual(result, '')

    def test_route_qualified(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst.route('home', 'a', _query={'b':'1'})
        self.assertEqual(result, 'http://example.com/a?b=1')

    def test_route_notqualified(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, False)
        result = inst.route('home', 'a', _query={'b':'1'})
        self.assertEqual(result, '/a?b=1')

    def test_route_qualified_override(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, False)
        result = inst.route('home', 'a', _query={'b':'1'}, _qualified=True)
        self.assertEqual(result, 'http://example.com/a?b=1')

    def test_route_notqualified_override(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst.route('home', 'a', _query={'b':'1'}, _qualified=False)
        self.assertEqual(result, '/a?b=1')

    def test___call__(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst('home', 'a', _query={'b':'1'})
        self.assertEqual(result, 'http://example.com/a?b=1')

    def test_current(self):
        self.config.add_route('home', '/')
        context = testing.DummyResource()
        request = testing.DummyRequest()
        request.matched_route = DummyRoute()
        inst = self._makeOne(context, request, True)
        result = inst.current('a', _query={'b':'1'})
        self.assertEqual(result, 'http://example.com/a?b=1')

    def test_resource(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        inst = self._makeOne(context, request, True)
        result = inst.resource('a', query={'b':'1'})
        self.assertEqual(result, 'http://example.com/a?b=1')

class DummyRoute(object):
    name = 'home'
    
