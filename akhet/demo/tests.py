import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import MyViews
        request = testing.DummyRequest()
        handler = MyViews(request)
        info = handler.index()
        self.assertEqual(info['project'], 'Akhet Demo')
