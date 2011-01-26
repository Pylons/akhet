Non-database Features
%%%%%%%%%%%%%%%%%%%%%

This chapter discusses the non-database features in pyramid_sqla's application
template.

Static files
============

This template takes a different approach to static files. The standard
templates use ``config.add_static_view`` to mount the static directory onto
the "/static" URL. This means all static files have to have the "/static"
prefix, so the top-level static assets -- "/favicon.ico", "/robots.txt", and
"/w3c_" (a machine-readable privacy policy) -- have to be served another way.

pyramid_sqla does some routing maneuvers to mount the static directory onto
"/", overlaying your dynamic URLs. This lets you serve all your static files
the same way. It's enabled by the following lines in *myapp/__init__.py*::

    from pyramid_sqla.static import add_static_route

    # Set up routes and views
    config.add_handler('home', '/', 'pyramidapp.handlers:MainHandler',
                       action='index')
    config.add_handler('main', '/{action}', 'pyramidapp.handlers:MainHandler',
        path_info=r'/(?!favicon\.ico|robots\.txt|w3c)')
    add_static_route(config, 'pyramidapp', 'static', cache_max_age=3600)

The first ``config.add_handler()`` call is an ordinary home page route, nothing
special about it. 

The second is a catchall route for "/{action}"; i.e., any one-component URL.
The ``path_info`` regex prevents the route from matching URLs referring to
top-level static assets. You'll have to do this with any routes that could
accidentally match your static URLs, which are generally routes with a variable
first component.

The ``add_static_route()`` call is a convenience function that mounts the
static directory onto "/". Then it just serves the files. If you look at the
wrapper's source code, it uses a custom route predicate so that if the implied
file doesn't exist, the route won't match the URL. This gives later routes or
traversal a chance to work, otherwise they would be blocked. 


.. _w3c: http://www.w3.org/P3P/ 

Helpers and the ``h`` variable
==============================

The *myapp/helpers.py* module is automatically available in templates as the
``h`` variable. This is borrowed from Pylons 1 and makes a convenient place to
put generic formatting functions or other convenience functions you use
throughout your templates.

You can also import the helpers module into your view handlers or other
code, but for that you'll have to do the import yourself.

The WebHelpers_ library contains a variety of helpers including an HTML tag
builder, form input tag builders, text and number formatting, etc. WebHelpers
is available separately in PyPI.

*Note:* ``webhelpers.paginate`` is not compatible with Pyramid unless you
provide a custom URL generation callback. A Pyramid-compatible alternative is
under development. The helpers in ``webhelpers.pylonslib`` are not compatible
with Pyramid due to their dependency on Pylons 1's magic globals. An
alternative system for flash messages and secure forms is built into Pyramid's
session object.

You can change which variables automatically appear in all templates. The code
is in *myapp/subscribers.py*.

Templates ending in .html
=========================

The app template arranges for all template files ending in .html to be served
by Mako. This is done by the following lines in *myapp/__init__.py*::

    config.add_renderer('.html', 'pyramid.mako_templating.renderer_factory')

You can change this to associate .html with another templating engine like
Jinja2, or disable it by commenting out the line.

Exception handling
==================

Pyramid's exception handling is the same as Pylons', although the syntax in
*development.ini* and *production.ini* is different. There is no top-level
'debug' variable. Instead, *development.ini* activates WebError's EvalException
middleware to show the sophisticated interactive traceback in the browser.

*production.ini* activates the ErrorMiddleware instead, which by default logs the
traceback to the console and displays a minimal error message to the user.
You can have the tracebacks emailed to you by adjusting the settings in
*production.ini*. Here are the default settings, which are pretty
self-explanatory:

.. code-block:: ini

    [filter:weberror]
    use = egg:WebError#error_catcher
    debug = false
    ;error_log = 
    ;show_exceptions_in_wsgi_errors = true
    ;smtp_server = localhost
    ;error_email = janitor@example.com
    ;smtp_username = janitor
    ;smtp_password = "janitor's password"
    ;from_address = paste@localhost
    ;error_subject_prefix = "Pyramid Error"
    ;smtp_use_tls =
    ;error_message =

The default error message shown to the user says::

    An error occurred. See the error logs for more information. (Turn debug on
    to display exception reports here) 

That is really more a reminder to you than a suitable message to the user. 
You can override the message by setting the 'error_message' variable.

If you set 'debug' to true in *production.ini*, a static traceback will be
shown to the user. This is not as harmful as the interactive traceback, but it does
reveal your application's structure.

**Do not use the EvalException middleware or 'debug = true' when running the
application exposed to the Internet.** Anybody who gets the interactive
traceback can enter any Python command, which may allow them to view or modify
arbitrary files or database data. The static traceback is not as harmful but it
does reveal your application's code structure.


.. _WebHelpers:  http://webhelpers.groovie.org/
