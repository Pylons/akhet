import logging

from pyramid.view import action

#from simpledemo.models import MyModel

log = logging.getLogger(__name__)

class MainHandler(object):
    def __init__(self, request):
        self.request = request

    @action(renderer='index.html')
    def index(self):
        log.debug("testing logging; entered MainHandler.index()")
        try:
            settings = self.request.registry.settings
        except AttributeError:
            # Kludge for default unit test: DummyRequest has no 'registry' attr
            settings = {}
        db_url = settings.get('sqlalchemy.url', 'UNKNOWN')
        return {'project':'simpledemo', 'db_url': db_url}
