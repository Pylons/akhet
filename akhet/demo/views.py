import logging

from pyramid.view import view_config

log = logging.getLogger(__name__)

class Handler(object):
    def __init__(self, request):
        self.request = request

class Main(Handler):

    @view_config(route_name="home", renderer="index.html")
    def index(self):
        # Do some logging.
        log.debug("testing logging; entered Main.index()")

        # Push a flash message if query param 'flash' is non-empty.
        if self.request.params.get("flash"):
            import random
            num = random.randint(0, 999999)
            message = "Random number of the day is:  %s." % num
            self.request.session.flash(message)
            # Normally you'd redirect at this point but we have nothing to
            # redirect to.

        # Return a dict of template variables for the renderer.
        return {"project": "Akhet Demo"}
