Details
%%%%%%%

development.ini
===============

The config file contains the following settings which aren't in Pyramid's
built-in scaffolds:

.. code-block:: ini

    mako.directories = akhet_demo:templates

    # Beaker cache
    cache.regions = default_term, second, short_term, long_term
    cache.type = memory
    cache.second.expire = 1
    cache.short_term.expire = 60
    cache.default_term.expire = 300
    cache.long_term.expire = 3600

    # Beaker sessions
    #session.type = file
    #session.data_dir = %(here)s/data/sessions/data
    #session.lock_dir = %(here)s/data/sessions/lock
    session.type = memory
    session.key = akhet_demo
    session.secret = 0cb243f53ad865a0f70099c0414ffe9cfcfe03ac

The "mako.includes" setting is necessary to set Mako's search path. You can add
other Mako options here if you wish.

The "cache." settings initialize Beaker caching. This is not actually necessary
because the demo never uses a cache, but it's here for demonstration.

The "session." settings initialize Beaker sessions. This is necessary if you
use sessions or flash messages. Beaker supports several forms of session
persistence: in-memory, files, memcached, database, etc. This configuration
uses memory mode, which holds the sessions in memory until the application
quits; it obviously works only with multi-threaded servers and not with than
multi-process serviers. The default Pylons mode is file-based sessions, which
is commented here. Recent recommendations suggest memcached is the most robust
mode because it can scale to multiple servers; you can set that option if you
wish.

If you copy the session configuration to your application, do change
"session.secret" to a random string. This is used to help ensure the integrity
of the session, to prevent people from hijacking it.


Init module and main function
=============================

Almost all of the *akhet_demo/__init__.py* module is unique to the demo, so
we'll just show the whole thing here:

.. code-block:: python
   :linenos:
    
    from pyramid.config import Configurator
    import pyramid_beaker

    def main(global_config, XXsettings):
        """ This function returns a Pyramid WSGI application.
        """
        config = Configurator(settings=settings)

        # Configure Beaker sessions and caching
        session_factory = pyramid_beaker.session_factory_from_settings(settings)
        config.set_session_factory(session_factory)
        pyramid_beaker.set_cache_regions_from_settings(settings)

        # Configure renderers and event subscribers.
        config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")
        config.include(".subscribers")
        config.include("akhet.static")

        # Add routes and views.
        config.add_route("home", "/")
        config.include("akhet.pony")
        config.add_static_route("akhet_demo", "static", cache_max_age=3600)
        config.scan()

        return config.make_wsgi_app()

(Note: "\*\*settings" is shown as "XXsettings" because vim's syntax
highlighting gets into a fit otherwise and mishighlights up the doc source file.) 

As you see, it activates Beaker sessions and caching, and sets up templates,
subscribers, routes, and a static route. The Beaker setup passes the
``settings`` dict to Beaker; that's how your settings are read. Pyramid
cofigures Mako the same way behind the scenes, passing the settings to it.
The "add_renderer" line tells Pyramid to recognize filenames ending in ".html"
as Mako templates. The subscribers include we'll see in a minute.

The static route has an include line and an "add_static_route" call. 


Helpers
=======

*akhet_demo/lib/helpers.py* is unique to the demo. It's a Pylons-like helpers
module where you can put utility functions for your templates. The minimal
WebHelpers imports for HTML tag helpers are there, but commented. I'm tempted
to actually use the tag helpers in the site template but haven't done so yet.

Most of WebHelpers works with Pyramid, including the popular
``webhelpers.html`` subpackage, ``webhelpers.text``, and ``webhelpers.number``.
Pyramid does not depend on WebHelpers so you'll have to add the dependency to
your application if you want to use it.  The only part that doesn't work with
Pyramid is the ``webhelpers.pylonslib`` subpackage, which depends on Pylons'
special globals.

WebHelpers 1.3 has some new URL generator classes to make it easier to use
with Pyramid. See the ``webhelpers.paginate`` documentation for details. (Note:
this is *not* the same as Akhet's URL generator; it's a different kind of class
specifically for the paginator's needs.)


Subscribers
===========

*akhet_demo/subscribers.py* is unique to the demo. It sets up a URL generator
and configures several Pylons-like globals for the template namespace. The only
thing you need in here is the includeme function, which the application's main
function invokes via the ``config.include(".subscribers")`` line.

The ``add_renderer_globals`` subscriber configures the following variables for
the template namespace:

* ``h``: the helpers module.
* ``r``: an alias for ``request``.
* ``url``: the URL generator.

It has commented code to configure "settings", "session", and "c" variables if
you want those.

For completeness, here are the system variables Pyramid 1.3 adds to the
template namespace:

* ``context``: the context.
* ``renderer_name``: the name of the renderer.
* ``renderer_info``: a ``RendererHelper`` object (defined in ``pyramid.renderers``).
* ``request``: the request.
* ``view``: the view. (A function or instance.)

As a reminder, everything here is local to the current request. The URL
generator is attached to the request object, and the renderer globals are set
just before the renderer is invoked. These variables are all discarded at the
end of the request.


Views
=====

The views module has a base class called ``Handler`` (but it's not related to
"pyramid_handlers").  The index view demonstrates logging, optionally sets a
flash message, and invokes a Mako template renderer.

:: 

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





.. include:: ../links.rst
