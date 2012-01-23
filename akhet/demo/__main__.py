import logging
from wsgiref.simple_server import make_server

import akhet.demo

def serve():
    """Run the application like 'pserve development.ini' would do."""

    settings = {
        "pyramid.reload_templates": True,
        "pyramid.debug_authorization": False,
        "pyramid.debug_notfound": False,
        "pyramid.debug_routematch": False,
        "pyramid.debug_templates": True,
        "pyramid.default_locale_name": "en",
        "pyramid.includes": ["pyramid_debugtoolbar"],
        "mako.directories": ["akhet.demo:templates"],
        }
    fmt = "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
    host = "127.0.0.1"
    port = 5000

    logging.basicConfig(level=logging.INFO, format=fmt)
    logging.getLogger("akhet.demo").setLevel(logging.DEBUG)

    app = akhet.demo.main({}, **settings)
    httpd = make_server(host, port, app)
    print('Starting HTTP server on http://%s:%s' % (host, port))
    httpd.serve_forever()

if __name__ == "__main__":  serve()
