Details
%%%%%%%%%%%%

pyramid.includes = pyramid_debugtoolbar
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




Init module and main function
=============================

::
    
    from pyramid.config import Configurator
    import pyramid_beaker

    def main(global_config, **settings):
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


Views
=============

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



Templates
=========

.html
site template
h, url, view
stylesheet, reset stylesheet


Site template
-------------

Most applications using Mako will define a site template something like this:

.. code-block:: mako

   <!DOCTYPE html>
   <html>
     <head>
       <title>${self.title()}</title>
       <link rel="stylesheet" href="${application_url}/default.css"
           type="text/css" />
     </head>
     <body>

   <!-- *** BEGIN page content *** -->
   ${self.body()}
   <!-- *** END page content *** -->
     </body>
   </html>
   <%def name="title()" />

Then the page templates can inherit it like so:

.. code-block:: mako

   <%inherit file="/site.html" />
   <%def name="title()">My Title</def>
   ... rest of page content goes here ...

Static files
============

Pyramid has five ways to serve static files. Each way has different
advantages and limitations, and requires a different way to generate static
URLs.

``config.add_static_route``

    This is the Akhet default,
    and is closest to Pylons. It serves the static directory as an overlay on
    "/", so that URL "/robots.txt" serves "zzz/static/robots.txt", and URL
    "/images/logo.png" serves "zzz/static/images/logo.png". If the file does
    not exist, the route will not match the URL and Pyramid will try the next
    route or traversal. You cannot use any of the URL generation methods with
    this; instead you can put a literal URL like
    "${application_url}/images/logo.png" in your template. 

    Usage::

        config.include('akhet')
        config.add_static_route('zzz', 'static', cache_max_age=3600)
        # Arg 1 is the Python package containing the static files.
        # Arg 2 is the subdirectory in the package containing the files.


Session, flash messages, and secure forms
=========================================

Pyramid's session object is ``request.session``. It has its own interface but
uses Beaker on the back end, and is configured in the INI file the same way as
Pylons' session. It's a dict-like object and can store any pickleable value.
It's pulled from persistent storage only if it's accessed during the request
processing, and it's (re)saved only if the data changes. 

Unlike Pylons' sesions, you don't have to call ``session.save()`` after adding
or replacing keys because Pyramid does that for you. But you do have to call
``session.changed()`` if you modify a mutable value in place (e.g., a session
value that's a list or dict) because Pyramid can't tell that child objects have
been modified.

You can call ``session.invalidate()`` to discard the session data at the end of
the request.  ``session.created`` is an integer timestamp in Unix ticks telling
when the session was created, and ``session.new`` is true if it was created
during this request (as opposed to being loaded from persistent storage).

Pyramid sessions have two extra features: flash messages and a secure form
token. These replace ``webhelpers.pylonslib.flash`` and
``webhelpers.pylonslib.secure_form``, which are incompatible with Pyramid.

Flash messages are a session-based queue. You can push a message to be
displayed on the next request, such as before redirecting. This is often used 
after form submissions, to push a success or failure message before redirecting
to the record's main screen. (This is different from form validation, which
normally redisplays the form with error messages if the data is rejected.)

To push a message, call ``request.session.flash("My message.")`` The message is
normally text but it can be any object. Your site template will then have to
call ``request.session.pop_flash()`` to retrieve the list of messages, and
display then as it wishes, perhaps in <div>'s or a <ul>. The queue is
automatically cleared when the messages are popped, to ensure they are
displayed only once.

The full signature for the flash method is::

    session.flash(message, queue='', allow_duplicate=True)

You can have as many message queues as you wish, each with a different string
name. You can use this to display warnings differently from errors, or to show
different kinds of messages at different places on the page. If
``allow_duplicate`` is false, the message will not be inserted if an identical
message already exists in that queue. The ``session.pop_flash`` method also takes a
queue argument to specify a queue. You can also use ``session.peek_flash`` to
look at the messages without deleting them from the queue.

The secure form token prevents cross-site request forgery (CSRF)
attacts. Call ``session.get_csrf_token()`` to get the session's token, which is
a random string. (The first time it's called, it will create a new random token and
store it in the session. Thereafter it will return the same token.) Put the
token in a hidden form field. When the form submission comes back in the next
request, call ``session.get_csrf_token()`` again and compare it to the hidden
field's value; they should be the same. If the form data is missing the field
or the value is different, reject the request, perhaps by returning a forbidden
status. ``session.new_csrf_token()`` always returns a new token, overwriting
the previous one if it exists.

WebHelpers and forms
====================

Most of WebHelpers works with Pyramid, including the popular
``webhelpers.html`` subpackage, ``webhelpers.text``, and ``webhelpers.number``.
Pyramid does not depend on WebHelpers so you'll have to add the dependency to
your application if you want to use it.  The only part that doesn't work with
Pyramid is the ``webhelpers.pylonslib`` subpackage, which depends on Pylons'
special globals.

We are working on a form demo that compares various form libraries: Deform,
Formish, FormEncode/htmlfill. 

To organize the form display-validate-action route, we recommend the
``pyramid_simpleform`` package. It replaces ``@validate`` in Pylons. It's not a
decorator because too many people found the decorator too inflexible: they
ended up copying part of the code into their action method.

WebHelpers 1.3 has some new URL generator classes to make it easier to use
with Pyramid. See the ``webhelpers.paginate`` documentation for details. (Note:
this is *not* the same as Akhet's URL generator; it's a different kind of class
specifically for the paginator's needs.)


.. include:: ../links.rst
