Akhet Architecture
%%%%%%%%%%%%%%%%%%%%%%%

Introduction
============

Here we'll go through the code in an Akhet application, explaining what each
part is and how it differs from Pylons. Some features come from Pyramid and are
common to Pyramid's built-in application skeletons, while others features are
added by Akhet. We'll try to specify which features come from where.

The sample application here is named "Zzz", and the top-level Python package
within it is "zzz". So wherever this manual says Zzz or zzz, it means your
actual application name or package name.

INI files
=========

development.ini
---------------

*development.ini* is generally similar to Pylons but has some different sections
and options:

.. code-block:: ini

    [app:myapp]
    use = egg:Zzz
    reload_templates = true
    debug_authorization = false
    debug_notfound = false
    debug_routematch = false
    debug_templates = true
    default_locale_name = en
    mako.directories = zzz:templates
    sqlalchemy.url = sqlite:///%(here)s/db.sqlite
    session.type = file
    session.data_dir = %(here)s/data/sessions/data
    session.lock_dir = %(here)s/data/sessions/lock
    session.key = Zzz
    session.secret = 4b391beb818275e9aef4a58207782e5366e9c662

.. code-block:: ini

    [server:main]
    use = egg:Paste#http
    host = 127.0.0.1
    port = 5000

.. code-block:: ini

    [pipeline:main]
    pipeline =
        egg:WebError#evalerror
        myapp

..
    The sections are in different code blocks due to a limitation in Pygments'
    syntax highlighting. If a value spans multiple lines as the "pipeline"
    value does, Pygments will not colorize any of the block.

The first thing to notice is that the main section is "[pipeline:main]", not
"[app:main]". In Pylons middleware is configured in middleware.py, but in
Pyramid it's configured in the INI file. Pyramid does not require any
middleware at all; we're only using it here for error handling.  

The default development pipeline has two components:

1. WebError's EvalError, which produces the interactive traceback if
   there's an uncaught exception.

2. "zzz" is the application, defined in the "[app:myapp]" section.

The "[app:myapp]" section has a "use = egg:Zzz" setting, which tells Paste to
load the Pyramid application by its entry point. An entry point is a shortcut
alias to a callable. The other variables in this section are arguments to that
callable, passed using ``\*\*kwargs`` so that the names can contain ".". The
actual callable is the ``main()`` function in the next section. Entry points
are defined in the application's *setup.py*.  More information on entry points
is in the Setup or Distribute documentation.

The "myapp" in the section name is always "myapp". All other "Zzz"'s in this
article are the actual name of your application, and "myapp"'s are the
corresponding package name. (Akhet hardcodes the section name to "myapp" so that
command-line utilities can guess which section contains the application
settings without having to ask the user.  "paster pshell" asks the user anyway,
but we're working on that.) 

The "debug\_\*" settings turn on various debugging features which output to the
console. "reload_templates" causes Mako to check the modify time of each
template before rendering it, to notice any changes. (It also works with
Chameleon and some other template engines.)

"sqlalchemy.url" is your database URL, the same as in Pylons. The "session.\*"
variables are the same as in Pylons. "session.secret" is automatically set to a
random number when the application is created.

The "[server:main]" section is the same as in Pylons. It tells which WSGI
server to run. By default this is PasteHTTPServer, a multhtreaded HTTP server
written in Pylons. 

production.ini
--------------

*production.ini* has a different pipeline:

.. code-block:: ini

    [pipeline:main]
    pipeline =
        weberror
        myapp

Here the WebError middleware replaces EvalException. This is exactly what
Pylons does; it's just configured a different way. Pylons has a global 'debug'
setting that indirectly choses WebError when false, while Pyramid just lets you
configure the middleware directly.
WebError dumps exception tracebacks to the console or emails them the
admistrator. It's is configured in the "[filter:weberror]" section:

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

Again, these are the same settings as Pylons' production.ini, just in a
different format.  

.. important::

   **To avoid security risks when running in production, ensure that
   EvalException is NOT used, and that WebError's debug setting is false.**
   The default production.ini does this, but you should double-check it anyway. 

   EvalException is useful during development, but if the application is
   exposed to the Internet and a malicious user gets the interactive traceback,
   either by accidentally getting an exception or by forcing an exception, s/he
   would have a Python prompt directly into your application's process, and
   could modify files or variables.

   WebError's debug mode is less dangerous but it does show an exception's
   traceback to the user, which may reveal details of your application
   structure and server environment that could be leveraged in an attack.

The "error_message" variable allows you to customize the error message shown to
the user if an exception occurs. The default message is rather unsatisfactory::

    Server Error

    An error occurred. See the error logs for more information. (Turn debug on
    to display exception reports here) 

This is more of a message to you than a meaningful message to the user, so you
may want to change it. Whatever text you put in the 'error_message' variable
will replace the second paragraph of the message. If you have a multi-line
message, indent the subsequent lines so that ConfigParser knows they're
continuation lines.

In the application section of *production.ini*, all the "debug\_\*" variables
and "reload_templates" are false. This saves some CPU cycles as it's processing
requests. 

Logging
-------

The bottom half of both INI files contain several sections to configure
Python's logging system.  This is the same as in Pylons. 

We can't explain the entire logging syntax here, but these are the sections
most often customized by users:

.. code-block:: ini

    [logger_root]
    level = WARN
    handlers = console

    [logger_zzz]
    level = DEBUG
    handlers =
    qualname = zzz

    [logger_sqlalchemy]
    level = INFO
    handlers =
    qualname = sqlalchemy.engine
    # "level = INFO" logs SQL queries.
    # "level = DEBUG" logs SQL queries and results.
    # "level = WARN" logs neither.  (Recommended for production systems.)

These define a logger "root", "zzz" (the application's package name), and
"sqlalchemy.engine" (specified in the qualname). Each has a 'level' variable
which can be DEBUG, INFO, WARN, ERROR, or CRITICAL. Each level also logs the
levels on its right, so WARN logs warnings and errors. Logger names are in a
dotted hierarchy, so that "sqlalchemy.engine" affects all loggers below it
("sqlalchemy.engine.ENGINE1", etc).  "root" affects all loggers that aren't
otherwise specified.

Generally, DEBUG is debugging information, INFO is chatty success messages,
WARN means something might be wrong, ERROR means something is
definitely wrong, and CRITICAL means you'd better fix it now or else. 
But each library can choose log at which level. So SQLAlchemy logs SQL queries
at the INFO level on "sqlalchemy.engine.ENGINE_NAME", even though some people
would consider this debugging information. 

Logger names do NOT automatically correspond to Python module names, although
it's customary to do so if there's no better name for the logger. That lets the
user quickly find the code that produced a log message.  In Akhet applications,
several loggers are predefined with the same name as the containing module.
E.g., ``zzz.helpers.main`` has the following code::

    import logging
    log = logging.getLogger(__name__)

This creates a variable ``log`` which is the "zzz.helpers.main" logger.
(``__name__`` is a special Python variable which is the name of the current
moduole.)

By default, *development.ini* sets the root logger to WARN, the application
logger to DEBUG, and the SQLAlchemy engine logger to INFO. This displays all
application logging and SQL queries, but suppresses all other messages unless
they're warnings or errors. *production.ini* sets all of these to WARN, to
avoid filling up your log files with trivial success messages. You can adjust
the log levels as you wish. You can also set other loggers to different levels
by creating a section for them and listing them in the "[loggers]" section.
they're warnings or errors. 

"paster serve" activates logging when it starts up. If you're not using "paster
serve", you can activate logging yourself this way::

    import logging.config
    logging.config.fileConfig(INI_FILENAME)

Init module
===========

A Pyramid application revolves around a top-level ``main()`` function in the
application package. "paster serve" does the equivalent of this::

    # Instantiate your WSGI application
    import zzz
    app = zzz.main(**settings)

The Pylons equivalent to ``main()`` is ``make_app()`` in middleware.py. The
``main()`` function replaces Pylons' middleware.py, config.py, *and* routing.py
but is much shorter:

.. code-block:: python
   :linenos:

    from pyramid.config import Configurator
    import akhet
    import pyramid_beaker
    import sqlahelper
    import sqlalchemy

    def main(global_config, XXsettings):
        """ This function returns a Pyramid WSGI application.
        """

        # Here you can insert any code to modify the ``settings`` dict.
        # You can:
        # * Add additional keys to serve as constants or "global variables" in the
        #   application.
        # * Set default values for settings that may have been omitted.
        # * Override settings that you don't want the user to change.
        # * Raise an exception if a setting is missing or invalid.
        # * Convert values from strings to their intended type.

        # Create the Pyramid Configurator.
        config = Configurator(settings=settings)
        config.include("pyramid_handlers")
        config.include("akhet")

        # Initialize database
        engine = sqlalchemy.engine_from_config(settings, prefix="sqlalchemy.")
        sqlahelper.add_engine(engine)
        config.include("pyramid_tm")

        # Configure Beaker sessions
        session_factory = pyramid_beaker.session_factory_from_settings(settings)
        config.set_session_factory(session_factory)

        # Configure renderers and event subscribers
        config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")
        config.add_subscriber("zzz.subscribers.create_url_generator",
            "pyramid.events.ContextFound")
        config.add_subscriber("zzz.subscribers.add_renderer_globals",
                              "pyramid.events.BeforeRender")

        # Set up view handlers
        config.include("zzz.handlers")

        # Set up other routes and views
        # ** If you have non-handler views, create create a ``zzz.views``
        # ** module for them and uncomment the next line.
        #
        #config.scan("zzz.views")

        # Mount a static view overlay onto "/". This will serve, e.g.:
        # ** "/robots.txt" from "zzz/static/robots.txt" and
        # ** "/images/logo.png" from "zzz/static/images/logo.png".
        #
        config.add_static_route("zzz", "static", cache_max_age=3600)

        # Mount a static subdirectory onto a URL path segment.
        # ** This not necessary when using add_static_route above, but it's the
        # ** standard Pyramid way to serve static files under a URL prefix (but
        # ** not top-level URLs such as "/robots.txt"). It can also serve files from
        # ** third-party packages, or point to an external HTTP server (a static
        # ** media server).
        # ** The first commented example serves URLs under "/static" from the
        # ** "zzz/static" directory. The second serves URLs under 
        # ** "/deform" from the third-party ``deform`` distribution.
        #
        #config.add_static_view("static", "zzz:static")
        #config.add_static_view("deform", "deform:static")

        return config.make_wsgi_app()

(Note: ``**settings`` in line 7 is displayed as ``XXsettings`` due to a
limitation in our documentation generator: "``*``" in code blocks
outside comments make Vim's syntax highlighting go bezerk.)

Lines 11-18 are a long comment explaining how you can modify the ``settings``
dict. If you have any code to set "global variables" for the application, or to
validate the settings or convert the values from strings to other types, 
put the code here. (We're considering a default routine to validate the
settings but haven't decided whether to use homegrown code, Colander,
FormEncode, or another validation library.)

Line 21 instantiates a ``Configurator`` which will create the application.
(It's not the application itself.) Lines 22-23 add plug-in functionality to
the configurator. The argument is the name of a module that contains an
``includeme()`` function. Line 22 ultimately creates the
``config.add_handler()`` method; line 23 creates the
``config.add_static_route()`` method. 

Line 26 creates a SQLAlchemy engine based on the "sqlalchemy.url" setting in
*development.ini*. The default setting is
"sqlite:///%(here)s/db.sqlite", which creates or opens a database "db.sqlite"
in the same directory as the INI file. You can also pass other engine arguments
to SQLAlchemy, either by putting them in the INI file with the "sqlalchemy."
prefix, or by passing them as keyword args. Line 27 adds the engine to the
``sqlahelper`` library so that the model can use it; it also updates the
library's contextual session.  Line 28 initializes the "pyramid_tm" transaction
manager. SQLAHelper is further explained in the Models section below; the
transaction manager is explained in the "Transaction Manager" chapter.

(Note: if you answered 'n' to the SQLAlchemy question when creating the
application, lines 4-5 and 25-28 will not be present in your module.)

Lines 31-32 configure the session factory. 

Line 35 tells Pyramid to render *\*.html* templates using Mako. Pyramid out of
the box renders Mako templates with the *\*.mako* or *\*.mak* extensions, and
Chameleon templates with the *\*.pt* extension, but you have to tell it if you
want to use a different extension or another template engine. Third-party
packages are available for using Jinja2 (``pyramid_jinja2``), and
a Genshi emulator using Chameleon (``pyramid_genshi_chameleon``),

Lines 36-39 registers event subscribers, which are callback functions called at
specific points during request processing. Lines 36-37 register a callback that
instantiates a URL generator (described in the Templates section below and in
the API_ chapter). Lines 38-39 register a callback which adds several
Pylons-like variables to the template namespace whenever a template is
rendered. The callbacks are defined in the ``zzz.subscribers`` module, which
you can modify.

Lines 42 configures routing. Actually it calls an include function in the
handlers package. We'll explore routing more fullyh later.

Lines 44-48 and 56-67 are commented code; they show how to enable certain
advanced features.

Line 54 is equivalent to the *public* directory in Pylons applications. It's
not a standard part of Pyramid, which handles static files a different way, but
this method is closer to the Pylons tradition. Any URLs which did not match a
dynamic route will be compared to the contents of the *zzz/static* directory,
and if a file exists for the URL, it is served. Unlike Pylons, this happens
after the dynamic routes are tried rather than before. This means that any
dynamic route that might accidentally match a static resource must explicitly
exclude that URL. 

This is just one of several ways to serve static files in Pyramid, each with
its own advantages and disadvantages. These are all discussed below in the
Static Files section.

Line 69 creates and returns a Pyramid WSGI application based on the
configuration.

This short main function -- compared to Pylons' three functions in three
modules -- allows an entire small application to be defined in a single module.
Half the lines are comments so they can be deleted.  A short main function is
useful for small demos, but the principle also leads to a different developer
culture. Pylons' application skeleton is complex enough that most people don't
stray from it, and Pylons' documentation emphasizes using "paster serve" rather
than other invocation methods. Pyramid's docs encourage users to structure
everything outside ``main()`` as they wish, and they describe "paster serve" as
just one way to invoke the application. The INI files and "paster serve" are
just for your convenience; you don't have to use them.

A bit more about Paster
-----------------------

"paster serve" does several other things besides calling the main function.
It interpolates "%(here)s" placeholders in the INI file, as well as
variables in the "[DEFAULT]" section (which we aren't using here). It
configures logging, and finds the application by looking up the entry point
specified in the 'use' variable. All this can be done by the following code
in both Pyramid and Pylons::

    import logging.config
    import os
    import paste.deploy.loadwsgi as loadwsgi
    ini_path = "/path/to/development.ini"
    logging.config.fileConfig(ini_path)
    app_dir, ini_file = os.path.split(ini_path)
    app = loadwsgi.loadapp("config:" + ini_file, relative_to=app_dir)

Models
======

The default *zzz/models/__init__.py* looks like this::

    import logging
    import sqlahelper
    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    import transaction

    log = logging.getLogger(__name__)

    Base = sqlahelper.get_base()
    Session = sqlahelper.get_session()


    #class MyModel(Base):
    #    __tablename__ = "models"
    #
    #    id = sa.Column(sa.Integer, primary_key=True)
    #    name = sa.Column(sa.Unicode(255), nullable=False)

Pylons applications have a "zzz.model.meta" model to hold SQLAlchemy's
housekeeping objects, but Akhet uses the SQLAHelper library which holds them
instead. This gives you more freedom to structure your models as you wish,
while still avoiding circular imports (which would happen if you defined
Session in the main module and then import the other modules into it; the
other modules would import the main module to get the Session, and voilà
circular imports).

A real application would replace the commented ``MyModel`` class with
one or more ORM classes. The example uses SQLAlchemy's "declarative" syntax,
although of course you don't have to. 

SQLAHelper
----------

The SQLAHelper library is a holding place for the application's contextual
session (normally assigned to a ``Session`` variable with a capital S, to
distinguish it from a regular SQLAlchemy session), all engines used by the
application, and an optional declarative base. We initialized it via the
``sqlahelper.add_engine`` line in the main function. Because we did not specify
an engine name, the library set the engine name to "default", and also bound the
contextual session and the base's metadata to it. 

There's not much else to know about SQLAHelper. You can call ``get_session()``
at any time to get the contextual session. You can call ``get_engine()`` or
``get_engine(name)`` to retrieve an engine that was previously added. You can
call ``get_base()`` to get the declarative base.  

If you need to modify the session-creation parameters, you can call
``get_session().config(...)``. But if you modify the session extensions, see
the "Transaction Manager" chapter to avoid losing the extension that powers the
transaction manager.

View handlers
=============

The default *zzz.handlers* package contains a *main* module which looks like
this::

    import logging

    from pyramid_handlers import action

    import zzz.handlers.base as base
    import zzz.models as model

    log = logging.getLogger(__name__)

    class Main(base.Handler):
        @action(renderer="index.html")
        def index(self):
            log.debug("testing logging; entered Main.index()")
            return {"project":"Zzz"}

This is clearly different from Pylons, and the ``@action`` decorator looks a
bit like TurboGears. The decorator has three optional arguments:

name
    
    The action name, which is the target of the route. Normally this is the
    same as the view method name but you can override it, and you must override
    it when stacking multiple actions on the same view method.

renderer

    A renderer name or template filename (whose extension indicates the
    renderer). A renderer converts the view's return value into a Response
    object. Template renderers expect the view to return a dict; other
    renderers may allow other types. Two non-template renderers are built into
    Pyramid: "json" serializes the return value to JSON, and "string" calls
    ``str()`` on the return value unless it's already a Unicode object. If you
    don't specify a renderer, the view must return a Response object (or any
    object having three particular attributes described in Pyramid's Response
    documentation). In all cases the view can return a Response object to
    bypass the renderer. HTTP errors such as HTTPNotFound also bypass the
    renderer.

permission

    A string permission name. This is discussed in the Authorization section
    below.

The Pyramid developers decided to go with the
return-a-dict approach because it helps in two use cases: 

1.  Unit testing, where you want to test the data calculated rather than
parsing the HTML output. This works by default because ``@action`` itself does
not modify the return value or arguments; it merely sets function attributes or
interacts with the configurator.

2. Situations where several URLs render the same data using different templates
or different renderers (like "json"). In that case, you can put multiple
``@action`` decorators on the same method, each with a different name and
renderer argument.

Two functions in ``pyramid.renderers`` are occasionally useful in views:

.. function:: pyramid.renderers.render(renderer_name, value, request=None, package=None)

    Render a template and return a string. 'renderer_name' is a template
    filename or renderer name. 'value' is a dict of template variables.
    'request' is the request, which is needed only if the template cares
    about it.

    If the function can't find the template, try passing "zzz:templates/"
    as the ``package`` arg.

.. function:: pyramid.renderers.render_to_response(renderer_name, value, request=None, package=None)

    Render a template, instantiate a Response, set the Response's body to
    the result of the rendering, and return the Response. The arguments are the
    same as for ``render()``, except that 'request' is more important.
    

The handler class inherits from a base class defined in *zzz.handlers.base*::

    """Base classes for view handlers.
    """

    class Handler(object):
        def __init__(self, request):
            self.request = request

            #c = self.request.tmpl_context
            #c.something_for_site_template = "Some value."

Pyramid does not require a base class but Akhet defines one for convenience. 
All handlers should set ``self.request`` in their ``.__init__`` method, and the
base handler does this. It also provides a place to put common methods used by
several handler classes, or to set ``tmpl_context`` (``c``) variables which are
used by your site template (common to all views or several views). (You
can use ``c`` in view methods the same way as in Pylons, although this is not
recommended.)

Note that non-template renders such as "json" ignore ``c`` variables, so it's
really only useful for HTML-only data like which stylesheet to use.

The routes are defined in *zzz/handlers/__init__.py*::

    """View handlers package.
    """

    def includeme(config):
        """Add the application's view handlers.
        """
        config.add_handler("home", "/", "zzz.handlers.main:Main",
                           action="index")
        config.add_handler("main", "/{action}", "zzz.handlers.main:Main",
            path_info=r"/(?!favicon\.ico|robots\.txt|w3c)")

``includeme`` is a configurator "include" function, which we've already seen.
This function calls ``config.add_handler`` twice to create two routes. The
first route connects URL "/" to the ``index`` view in the ``Main`` handler.

The second route connects all other one-segment URLs (such as "/hello" or
"/help") to a same-name method in the ``Main`` handler. "{action}" is a path
variable which will be set the corresponding substring in the URL. Pyramid will
look for a method in the handler with the same action name, which can either be
the method's own name or another name specified in the 'name' argument to
``@action``. Of course, these other methods ("hello" and "help") don't exist in
the example, so Pyramid will return 400 Not Found status. 

The 'path_info' argument is a regex which excludes certain URLs from matching
("/favicon.ico", "/robots.txt", "/w3c"). These are static files or directories
that would syntactically match "/{action}", but we want these to go to a later
route instead (the static route). So we set a 'path_info' regex that doesn't
match them.

Redirecting and HTTP errors
---------------------------

To issue a redirect inside a view, return an HTTPFound::

    from pyramid.httpexceptions import HTTPFound

    def myview(self):
        return HTTPFound(location=request.route_url("foo"))
        # Or to redirect to an external site
        return HTTPFound(location="http://example.com/")

You can return other HTTP errors the same way: ``HTTPNotFound``, ``HTTPGone``,
``HTTPForbidden``, ``HTTPUnauthorized``, ``HTTPInternalServerError``, etc.
These are all subclasses of both ``Response`` and ``Exception``.  Although you
can raise them, Pyramid prefers that you return them instead.

If you intend to raise them, you have to do two extra things. One, define an
exception view for each one that returns the exception object itself
(``request.exception``). Two, if you want to be compatible with Python 2.4 and
2.3, do ``raise HTTPNotFound().exception()`` rather than raising the instance
directly. HTTP exceptions are new-style classes which can't be raised in Python
2.4 or 2.3.  See the Views chapter in the Pyramid manual for details on
exception views and raising HTTP exceptions.

Pyramid catches two non-HTTP exceptions by default,
``pyramid.exceptions.NotFound`` and ``pyramid.exceptions.Forbidden``, which
it sends to the Not Found View and the Forbidden View respectively. You can
override these views to display custom HTML pages.

More on routing and traversal
=============================

Routing methods and view decorators
-----------------------------------

Pyramid has several routing methods and view decorators. The ones we've seen,
from the ``pyramid_handlers`` package, are:

.. function:: @action(\*\*kw)

   I make a method in a class into a *view* method, which
   ``config.add_handler`` can connect to a URL pattern. By definition, any class
   that contains view methods is a view handler. My most interesting args are 
   'name' and 'renderer'. If 'name' is NOT specified, the action name is the
   same as the method name. If 'name' IS specified, the action name can be
   different. If 'renderer' is specified, it indicates a renderer or template
   (and the template's extension indicates a renderer). If multiple ``@action``
   decorators are put on a single method, each must have a different name, and
   they presumably will have different renderers too.

.. method:: config.add_handler(name, pattern, handler, action=None, \*\*kw)

   I create a route connecting the URL pattern to the handler class. If
   'action' is specified, I connect the route to that specific action (a method
   decorated with the ``@action`` decorator). If 'action' is not specified, the
   pattern must contain a "{action}" placeholder. In that case I scan the
   handler class for all possible actions. It is an error to specify both "{action}"
   and an ``action`` arg. I pass extra keyword args to ``config.add_route``,
   and keyword args in the ``@action`` decorator to ``config.add_view``.

``config.add_handler`` calls two lower-level methods which you can also call
directly:

.. method:: config.add_route(name, pattern, \*\*kw)

   Create a route connecting a URL pattern directly to a view callable outside
   a handler.  The view is specified with a 'view' arg. If the view is a
   function, it must take a Request argument and return a Response (or any
   object with the three required attributes). If it's a class, the constructor
   takes the Request argument and the specified method (``.__call__`` by
   default) is called with no arguments.

.. method:: config.add_view(\*\*kw)

   I register a view (specified with a 'view' arg). In URL dispatch, you
   normally don't call this directly but let ``config.add_handler`` or
   ``config.add_route`` call it for you. In traversal, you call this to
   register a view. The 'name' argument is the view name, which is used by
   traversal to choose which view to invoke.

Two others you should know about:

.. function:: config.scan(package=None)

   I scan the specified package (which may be an asset spec) and import all its
   modules recursively, looking for functions decorated with ``@view_config``.
   For each such function, I call ``add_view`` passing the decorator's args to
   it. I can also scan a package, in which case all submodules in the package
   are recursively scanned. If no package is specified, I scan the caller's
   package (i.e., the entire application). 
   
   I can also be called for my side effect of importing all of a package's
   modules even if none of them contain ``@view_config``.

.. function:: @view_config(\*\*kw)

   I decorate a function so that ``config.scan`` will recognize it as a view
   callable, and I also hold ``add_view`` arguments that ``config.scan`` will
   pick up and apply.  I can also decorate a class or a method in a class.


Route arguments and predicates
------------------------------

``config.add_handler`` accepts a large number of keyword
arguments. We'll list the ones most commonly used with Pylons-like applications
here. For full documentation see the `add_route
<http://docs.pylonsproject.org/projects/pyramid/1.0/api/config.html#pyramid.config.Configurator.add_route>`_
API. Most of these arguments can also be used with ``config.add_route``.

The arguments are divided into *predicate arguments* and *non-predicate
arguments*.  Predicate arguments determine whether the route matches the
current request: all predicates must pass in order for the route to be chosen.
Non-predicate arguments do not affect whether the route matches.

name

    [Non-predicate] The first positional arg; required. This must be a unique
    name for the route, and is used in views and templates to generate the URL.

pattern

    [Predicate] The second positional arg; required. This is the URL path with
    optional "{variable}" placeholders; e.g., "/articles/{id}" or
    "/abc/{filename}.html". The leading slash is optional. By default the
    placeholder matches all characters up to a slash, but you can specify a
    regex to make it match less (e.g., "{variable:\d+}" for a numeric variable)
    or more ("{variable:.*}" to match the entire rest of the URL including
    slashes). The substrings matched by the placeholders will be available as
    *request.matchdict* in the view.

    A wildcard syntax "\*varname" matches the rest of the URL and puts it into
    the matchdict as a tuple of segments instead of a single string.  So a
    pattern "/foo/{action}/\*fizzle" would match a URL "/foo/edit/a/1" and
    produce a matchdict ``{'action': u'edit', 'fizzle': (u'a', u'1')}``.

    Two special wildcards exist, "\*traverse" and "\*subpath". These are used
    in advanced cases to do traversal on the right side of the URL, and should
    be avoided otherwise.

factory

    [Non-predicate] A callable (or asset spec). In URL dispatch, this returns a
    *root resource* which is also used as the *context*. If you don't specify
    this, a default root will be used. In traversal, the root contains one
    or more resources, and one of them will be chosen as the context.

xhr

    [Predicate] True if the request must have an "X-Reqested-With" header. Some
    Javascript libraries (JQuery, Prototype, etc) set this header in AJAX
    requests.

request_method

    [Predicate] An HTTP method: "GET", "POST", "HEAD", "DELETE", "PUT". Only
    requests of this type will match the route.

path_info

    [Predicate] A regex compared to the URL path (the part of the URL after the
    application prefix but before the query string). The URL must match this
    regex in order for the route to match the request.

request_param

    [Predicate] If the value doesn't contain "=" (e.g., "q"), the request must
    have the specified parameter (a GET or POST variable). If it does contain
    "=" (e.g., "name=value"), the parameter must have the specified value.

    This is especially useful when tunnelling other HTTP methods via
    POST. Web browsers can't submit a PUT or DELETE method via a form, so it's
    customary to use POST and to set a parameter ``_method="PUT"``. The
    framework or application sees the "_method" parameter and pretends the
    other HTTP method was requested. In Pyramid you can do this with
    ``request_param="_method=PUT``.

header

    [Predicate] If the value doesn't contain ":"; it  specifies an HTTP header
    which must be present in the request (e.g., "If-Modified-Since"). If it
    does contain ":", the right side is a regex which the header value must
    match; e.g., "User-Agent:Mozilla/.\*". The header name is case insensitive.

accept

    [Predicate] A MIME type such as "text/plain", or a wildcard MIME type with
    a star on the right side ("text/\*") or two stars ("\*/\*"). The request
    must have an "Accept:" header containing a matching MIME type.

custom_predicates

    [Predicate] A sequence of callables which will be called in order to
    determine whether the route matches the request. The callables should
    return ``True`` or ``False``. If any callable returns ``False``, the route
    will not match the request. The callables are called with two arguments,
    ``info`` and ``request``. ``request`` is the current request. ``info`` is a
    dict which contains the following::
    
        info["match"]  =>  the match dict for the current route
        info["route"].name  =>  the name of the current route
        info["route"].pattern  =>  the URL pattern of the current route

    Use custom predicates argument when none of the other predicate args fit
    your situation.  See
    <http://docs.pylonsproject.org/projects/pyramid/1.0/narr/urldispatch.html#custom-route-predicates>`
    in the Pyramid manual for examples.

    You can modify the match dict to affect how the view will see it. For
    instance, you can look up a model object based on its ID and put the object
    in the match dict under another key. If the record is not found in the
    model, you can return False to prevent the route from matching the request;
    this will ultimately case HTTPNotFound if no other route or traversal
    matches the URL.  The difference between doing this and returning
    HTTPNotFound in the view is that in the latter case the following routes
    and traversal will never be consulted. That may or may not be an advantage
    depending on your application.

View arguments
--------------

The 'name', 'renderer' and 'permission' arguments described for ``@action`` can
also be used with ``@view_config`` and ``config.add_view``.

``config.add_route`` has counterparts to some of these such as
'view_permission'.

``config.add_view`` also accepts a 'view' arg which is a view callable or asset
spec. This arg is not useful for the decorators which already know the view.

The 'wrapper' arg can specify another view, which will be called when this view
returns. (XXX Is this compatible with view handlers?)


The request object
==================

The Request object contains all information about the current request state and
application state. It's available as ``self.request`` in handler views, the
``request`` arg in view functions, and the ``request`` variable in templates.
In pshell or unit tests you can get it via 
``pyramid.threadlocal.get_current_request()``. (You shouldn't use the
threadlocal back door in most other cases. If something you call from the view
requires it, pass it as an argument.)

Pyramid's ``Request`` object is a subclass of WebOb Request just like
'pylons.request' is, so it contains all the same attributes in methods like
``params``, ``GET``, ``POST``, ``headers``, ``method``, ``charset``, ``date``,
``environ``, ``body``, and ``body_file``. The most commonly-used attribute is
``request.params``, which is the query parameters and POST variables.

Pyramid adds several attributes and methods. ``context``, ``matchdict``,
``matched_route``, ``registry``, ``registry.settings``, ``session``, and
``tmpl_context`` access the request's state data and global application data. 
``route_path``, ``route_url``, ``resource_url``, and ``static_url`` generate
URLs, shadowing the functions in ``pyramid.url``. (One function,
``current_route_url``, is available only as a function.)

Rather than repeating the existing documentation for these attributes and
methods, we'll just refer you to the original docs:

* `Pyramd Request, Response, HTTP Exceptions, and MultiDict <http://docs.pylonsproject.org/projects/pyramid/1.0/narr/webob.html>`_
* `Pyramid Request API <http://docs.pylonsproject.org/projects/pyramid/1.0/api/request.html#request-module>`_
* `WebOb Request API <http://pythonpaste.org/webob/reference.html#id1>`_
* `Pyramid Response API <http://docs.pylonsproject.org/projects/pyramid/1.0/api/response.html>`_
* `WebOb Response API <http://pythonpaste.org/webob/reference.html#id2>`_

MultiDict is not well documented so we've written our own `MultiDict API`_
page. In short, it's a dict-like object that can have multiple values for each
key.  ``request.params``, ``request.GET``, and ``request.POST`` are MultiDicts.

Pyramid has no pre-existing Response object when your view starts executing. To
change the response status type or headers, you can either instantiate your own
``pyramid.response.Response`` object and return it, or use these special
Request attributes defined by Pyramid::

    request.response_status = "200 OK"
    request.response_content_type = "text/html"
    request.response_charset = "utf-8"
    request.response_headerlist = [
        ('Set-Cookie', 'abc=123'), ('X-My-Header', 'foo')]
    request.response_cache_for = 3600    # Seconds

Akhet adds one Request attribute. ``request.url_generator``, which is used to
implement the ``url`` template global described below.


Templates
=========

Pyramid has built-in support for Mako and Chameleon templates. Chameleon runs
only on CPython and Google App Engine, not on Jython or other platforms. Jinja2
support is available via the ``pyramid_jinja2`` package on PyPI, and a Genshi
emulator using Chameleon is in the ``pyramid_chameleon_genshi`` package.

Whenever a renderer invokes a template, the template namespace includes all the
variables in the view's return dict, plus the following:

.. attribute:: request

   The current request.

.. attribute:: context

   The context (same as ``request.context``).

.. attribute:: renderer_name

   The fully-qualified renderer name; e.g., "zzz:templates/foo.mako".

.. attribute:: renderer_info

   An object with attributes ``name``, ``package``, and ``type``.

The subscriber in your application adds the following additional variables:

.. attribute:: c, tmpl_context

   ``request.tmpl_context``

.. attribute:: h

   The helpers module, defined as "zzz.helpers". This is set by a subscriber
   callback in your application; it is not built into Pyramid. 

.. attribute:: session

   ``request.session``.

.. attribute:: url

   In Akhet, a URLGenerator object. In Pyramid's built-in application templates
   that use URL dispatch, an alias to the ``route_url`` *function*, which
   requires you to pass the route name as the first arg and the request as the
   second arg.

   The URLGenerator object has convenience methods for generating URLs based on
   your application's routes. See the complete list on the API_ page.

   By default the generator creates unqualified URLs (i.e., without the
   "scheme://hostname" prefix) if the underlying Pyramid functions allow it.
   To get absolute URLs throughout the application, edit *zzz/subscribers.py*,
   go to the line where the URLGenerator is instantiated, and change the
   'qualified' argument to True. Pylons traditionally uses unqualified URLs,
   while Pyramid traditionally uses qualified URLs. Note that qualified URLs
   may be wrong if the application is running behind a reverse proxy! (E.g.,
   Apache's mod_proxy.) The generated URL may be "http://localhost:5000" which
   is correct for the application but invalid to the end user (who needs the
   proxy's URL, "https://example.com").  

Advanced template usage
-----------------------

If you need to fill a template within view code or elsewhere, do this::

    from pyramid.renderers import render
    variables = {"foo": "bar"}
    html = render("mytemplate.mako", variables, request=request)

There's also a ``render_to_response`` function which invokes the template and
returns a Response, but usually it's easier to let ``@action`` or
``@view_config`` do this. However, if your view has an if-stanza that needs to
override the template specified in the decorator, ``render_to_response`` is
the way to do it. ::

    @action(renderer="index.html")
    def index(self):
        records = models.MyModel.all()
        if not records:
            return render_to_response("no_records.html")
        return {"records": records}

For further information on templating see the Templates section in the Pyramid
manual, the Mako manual, and the Chameleon manual.  You can customize Mako's
TemplateLookup by setting "mako.*" variables in the INI file.

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

``config.add_static_view``

    This is Pyramid's default algorithm. It mounts a static directory under a
    URL prefix such as "/static". It is not an overlay; it takes over the URL
    prefix completely. So URL "/static/images/logo.png" serves file
    "zzz/static/images/logo.png". You cannot serve top-level static files like
    "/robots.txt" and "/favicon.ico" using this method; you'll have to serve
    them another way. 

    Usage::

        config.add_static_view("static", "zzz:static")
        # Arg 1 is the view name which is also the URL prefix.
        # It can also be the URL of an external static webserver.
        # Arg 2 is an asset spec referring to the static directory/

    To generate "/static/images/logo.png" in a Mako template, which will serve
    "zzz/static/images/logo.png":

    .. code-block:: mako

       href="${request.static_url('zzz:static/images/logo.png')}

    One advantage of add_static_view is that you can copy the static directory
    to an external static webserver in production, and static_url will
    automatically generate the external URL:

    .. code-block:: ini

        # In INI file
        static_assets = "static"
        # -OR-
        static_assets = "http://staticserver.com/"

    ..  code-block:: python

        config.add_static_view(settings["static_assets"], "zzz:static")

    .. code-block:: mako

        href="${request.static_url('zzz:static/images/logo.png')}"
        ## Generates URL "http://staticserver.com/static/images/logo.png"

Other ways

    There are three other ways to serve static files. One is to write a custom
    view callable to serve the file; an example is in the Static Assets section
    of the Pyramid manual. Another is to use ``paste.fileapp.FileApp`` or
    ``paste.fileapp.DirectoryApp`` in a view. (More recent versions are in the
    "PasteOb" distribution.) These three ways can be used with
    ``request.route_url()`` because the route is an ordinary route. The
    advantage of these three ways is that they can serve a static file or
    directory from a normal view callable, and the view can be protected
    separately using the usual authorization mechanism.

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

WebHelpers 1.3b1 has some new URL generator classes to make it easier to use
with Pyramid. See the ``webhelpers.paginate`` documentation for details. (Note:
this is *not* the same as Akhet's URL generator; it's a different kind of class
specifically for the paginator's needs.)


Shell
=====

**paster pshell** is similar to Pylons' "paster shell". It gives you an
interactive shell in the application's namespace with a dummy request. Unlike
Pylons, you have to specify the application section on the command line because
it's not "main". Akhet, for convenience, names the section "myapp" regardless
of the actual application name. 

.. code-block:: sh

    $ paster pshell development.ini myapp
    Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39) 
    [GCC 4.4.5] on linux2
    Type "help" for more information. "root" is the Pyramid app root object, "registry" is the Pyramid registry object.
    >>> registry.settings["sqlalchemy.url"]
    'sqlite:////home/sluggo/exp/pyramid-docs/main/workspace/Zzz/db.sqlite'
    >>> import pyramid.threadlocal
    >>> request = pyramid.threadlocal.get_current_request()
    >>> 

As the example above shows, the interactice namespace contains two objects
initially: ``root`` which is the root object, and ``registry`` from which you
can access the settings. To get the request, you have to use Pyramid's
threadlocal library to fetch it. This is one of the few places where it's
recommended to use the threadlocal library.

Deployment
==========

Deployment is the same for Pyramid as for Pylons. Use "paster serve" with
mod_proxy, or mod_wsgi, or whatever else you prefer. 


.. _MultiDict API: api.html#multidict
.. _API: api.html
