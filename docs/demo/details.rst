Details
%%%%%%%

development.ini
===============

The config file contains the following settings which aren't in Pyramid's
built-in scaffolds:

* mako.directories: necessary when using Mako, to set the template search
  path. (Theoretically you don't need this if you specify renderers by asset
  spec rather than by relative path, but I couldn't get that to work.)
* cache.\*:  Beaker cache settings. These are not actually necessary because
  the demo never uses a cache, but they're here for demonstration.
* session.\*: Beaker session settings. These are necessary if you use sessions
  or flash messages.

Beaker supports several kinds of session
persistence: in-memory, files, memcached, database, etc. The demo's
configuration uses memory mode, which holds the sessions in memory until the application
quits. It contains commented settings for file-based sessions, which is Pylons'
default. Experienced developers seem to be choosing memcached mode nowadays.
Memory sessions disappear when the server is restarted, and work only with
multithreaded servers, not multiprocess servers. File-based sessions are
persistent, but add the complications of a directory and permissions and
maintenance. Memcached avoids all these problems, and it also scales to
multiple parallel servers, which can all share a memcached session.

If you copy the session configuration to your application, do change
"session.secret" to a random string. This is used to help ensure the integrity
of the session, to prevent people from hijacking it.


Init module and main function
=============================

The main function, in addition to the minimal Pyramid configuration, activates
Beaker sessions and caching, and sets up templates, subscribers, routes, and a
static route. The Beaker setup passes the ``settings`` dict to Beaker; that's
how your settings are read. Pyramid cofigures Mako the same way behind the
scenes, passing the settings to it.  The "add_renderer" line tells Pyramid to
recognize filenames ending in ".html" as Mako templates. The subscribers
include we'll see in a minute.

Activating static routes involves an include line and a "config.add_static_route"
call.


Helpers
=======

The demo provides a Pylons-like helpers module, 
*akhet_demo/lib/helpers.py*. You can put utility functions here for use in
your templates. The helper contains imports for WebHelper's HTML tag helpers,
but they're commented out. (WebHelpers is a Python package containing generic
functions for use in web applications and other applications.) I'm tempted to
actually use the tag helpers in the site template but haven't done so yet.

Most of WebHelpers works with Pyramid, including the popular
``webhelpers.html`` subpackage, ``webhelpers.text``, and ``webhelpers.number``.
You'll have to add a WebHelpers dependency to your application if you want to
use it.  The only part of WebHelpers that doesn't work with Pyramid is the
``webhelpers.pylonslib`` subpackage, which depends on Pylons' special globals.

Note that ``webhelpers.paginate`` requires a slightly different configuration
with Pyramid than with Pylons, because ``pylons.url`` is not available. You'll
have to supply a URL generator, perhaps using one of the convenience classes
included in WebHelpers 1.3. Paginate's URL generator is *not* Akhet's URL
generator: it's a different kind of class specific to the paginator's needs.


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

The demo pushes a flash message by calling ``self.request.session.flash()``
with the message text. By default this puts the message on the "info" queue,
and it's displayed using an "info" CSS class. You can push the message onto a
different queue by specifying the queue name as a second argument. But that's
only useful if the template pops the messages from the other queue by name,
otherwise they'll never be displayed. It's customary to name the queues
according to the Python logging hierarchy: debug, info (notice), warn(ing),
error, critical. The default stylesheet defines CSS classes with distinct
styling for several of these levels.


.. include:: ../links.rst
