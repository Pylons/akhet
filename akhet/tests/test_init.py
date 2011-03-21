import unittest
import akhet

class Test_includeme(unittest.TestCase):
    def _callFUT(self, config):
        return akhet.includeme(config)

    def test_it(self):
        from akhet.static import add_static_route
        config = DummyConfig()
        self._callFUT(config)
        self.assertEqual(config.directives["add_static_route"],
                         add_static_route)


class DummyConfig(object):
    def __init__(self):
        self.routes = []
        self.directives = {}

    def add_directive(self, name, value):
        self.directives[name] = value
