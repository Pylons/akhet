Pyramid Architecture
%%%%%%%%%%%%%%%%%%%%

This chapter walks through the default 'alchemy' application you created in the
last chapter (or downloaded the tarball). We'll skim just briefly over material
that's covered in the Wiki tutorial, instead focusing on how Pyramid differs
from Pylons.

The Zzz application has several aspects similar to Pylons: INI
files, a startup function, views (called Controllers in Pylons), templates, and
models. However, the filenames are different and the API syntax is
different.  Pyramid is more flexible than Pylons, so you can create a `minimal
application`_ in a single Python module, and run it in the same module without
an INI file or "pserve".  However, we'll stick to the 'alchemy' scaffold which
creates a directory structure scalable to large applications.

Directory layout
----------------

The default application contains the following files after you install
it:

.. code-block::  text

    Zzz
    ├── CHANGES.txt
    ├── MANIFEST.in
    ├── README.txt
    ├── development.ini
    ├── production.ini
    ├── setup.cfg
    ├── setup.py
    ├── zzz
    │   ├── __init__.py
    │   ├── models.py
    │   ├── scripts
    │   │   ├── __init__.py
    │   │   └── populate.py
    │   ├── static
    │   │   ├── favicon.ico
    │   │   ├── footerbg.png
    │   │   ├── headerbg.png
    │   │   ├── ie6.css
    │   │   ├── middlebg.png
    │   │   ├── pylons.css
    │   │   ├── pyramid.png
    │   │   ├── pyramid-small.png
    │   │   └── transparent.gif
    │   ├── templates
    │   │   └── mytemplate.pt
    │   ├── tests.py
    │   └── views.py
    └── Zzz.egg-info
        ├── dependency_links.txt
        ├── entry_points.txt
        ├── not-zip-safe
        ├── PKG-INFO
        ├── requires.txt
        ├── SOURCES.txt
        └── top_level.txt

..
   Generated via this command and manually resorted and some entries removed.
   tree --noreport -n -I '*.pyc' Zzz  >/tmp/files

development.ini
---------------

*development.ini* has the same structure as Pylons, and it's actually simpler
than earlier versions of Pyramid. The application and server sections look like
this:

.. code-block:: ini

    [app:main]
    use = egg:Zzz

    pyramid.reload_templates = true
    pyramid.debug_authorization = false
    pyramid.debug_notfound = false
    pyramid.debug_routematch = false
    pyramid.debug_templates = true
    pyramid.default_locale_name = en
    pyramid.includes = pyramid_debugtoolbar
                       pyramid_tm

    sqlalchemy.url = sqlite:///%(here)s/Zzz.db

    [server:main]
    use = egg:pyramid#wsgiref
    host = 0.0.0.0
    port = 6543

The logging sections will be covered in the logging chapter. Differences
between development.ini and production.ini will be covered in the deployment
chapter.

When you run "pserve development.ini", it does the following:

1. Activate logging based on the logging sections.
2. Read the "[app:main]" section and instantiate the specified application.
3. Read the "[server:main]" section and instantiate the specified server.
4. Launch the server with the application, and let it process requests forever.

In the app section, the "use = egg:Zzz" tells which Python distribution to
load, in this case our "Zzz" application. The "pyramid.\*" options are mostly
debugging variables.  Set any of them to "true" to enable various kinds of
debug logging.  "pyramid.default_locale_name" sets the predominent
region/language for the application.  "pyramid.reload_templates" tells whether
to recheck the timestamp of template source files whenever it renders a
template, in case the file has been updated since startup. (Mako and Chameleon
respect this value, but not all template engines understand it.)

"pyramid_includes" specifies optional "tweens" to wrap around the application.
Tweens are like WSGI middleware but are specific to Pyramid. In other words,
they're generic services that can be wrapped around a variety of applications.
"pyramid_debugtoolbar" is the debug toolbar at the right margin of browser
screens, and shows an interactive traceback screen if an exception occurs.
"pyramid_tm" is the transaction manager, which is covered in a later chapter.

(To see the interactive traceback in action, skip the "populate_Zzz" step or
delete the "Zzz.db" file, and run pserve. It will error out because a
database table doesn't exist. If it doesn't give an error, add a ``raise
RuntimeError`` line in the ``my_view`` function in *zzz/views.py*.)

"sqlalchemy.url" tells which database the application should use. "%(here)s"
expands to the path of the directory containing the INI file.

The "[server:main]" section is the same as in Pylons. It tells which WSGI
server to run. Pyramid 1.3 defaults to the wsgiref HTTP server in the
Python standard library. It's single-threaded so it can only handle one request
at a time, but that's good enough for development or debugging. 

Pyramid no longer uses WSGI middleware by default. If you want to add your own
middleware, see the `PasteDeploy manual`_ for the syntax. But first consider
whether making a Pyramid tween would be more convenient.



Init module and main function
=============================

A Pyramid application revolves around a top-level ``main()`` function in the
application package. "pserve" does the equivalent of this::

    # Instantiate your WSGI application
    import zzz
    app = zzz.main(**settings)

The Pylons equivalent to ``main()`` is ``make_app()`` in middleware.py. The
``main()`` function replaces Pylons' middleware.py, config.py, *and* routing.py
but is much shorter:

.. code-block:: python
   :linenos:

    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config

    from .models import DBSession

    def main(global_config, XXsettings):
        """ This function returns a Pyramid WSGI application.
        """
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        config = Configurator(settings=settings)
        config.add_static_view('static', 'static', cache_max_age=3600)
        config.add_route('home', '/')
        config.scan()
        return config.make_wsgi_app()

(*Doc limitation*: ``XXsettings`` in line 6 is actually ``**settings``.
We had to alter it in the docs to prevent Vim's syntax highlighting from going
bezerk.)

This main function is short and sweet. Later we'll discuss lots of things you
can add here to add features.

"pserve" parses the "[app:main]" options into a dict called "settings". It
calls the ``main()`` function with the settings as keyword args. (The
``global_config`` arg is not used much; it's covered later.)

Lines 9-10 instantiate a database engine based on the "sqlalchemy." settings in
the INI file. ``DBSession`` is a global object used to access SQLAlchemy's
object-relational mapper (ORM). 

Line 11 instantiates a ``Configurator`` which will instantiate the application.
(It's not the application itself.)

Line 12 tells the configurator to serve the static directory (*zzz/static*)
under URL "/static". The arguments are more than they appear, as we'll see in
the customization section.

Line 13 creates a route for the home page. This is more or less like a Pylons
route, except it doesn't specify a controller and action. 

Line 14 scans the application's Python modules looking for views to register.
This imports all the modules under ``zzz``.

Line 15 instantiates a Pyramid WSGI application based on the configuration, and
returns it.

Configurator constructor arguments
----------------------------------

The Configurator constructor accepts the following optional arguments:

authentication_policy, authorization_policy

    Callbacks to enable Pyramid's built-in authorization mechanism. The
    Authorizatoin chapter in the Wiki tutorial has an example of their use.

root_factory

    A callback that returns a *resource root*. See next section.
    has an extra piece of data called the *context*. 
    this, so Pyramid uses a default factory that always returns ``None``.
    value called the *context* 
    the *context* 
    deliveredc to the view as its *context*. In URL dispatch, the root will be
    delivered directly to the view as the *context*. The example does *not*
    specify this argument, so Pyramid uses a default root factory that always
    delivers ``None`` as a context. The Wiki tutorial

    

Note that the ``Configurator`` constructor does *not* have a ``root_factory=``
argument. In URL dispatch, root factories are used only in advanced cases.
The argument is a 
mainly to set authorization permissions or as a fancy way to deliver database
objects to the view. 
mainly to set up authorization permissions or to deliver database objects to
the view. Pyramid will fall back to a default root factory, which always
delivers a ``None`` context to the view.

Route arguments and predicates
------------------------------

``config.add_route`` accepts a large number of keyword
arguments. Here are the ones most commonly used in Pylons-like applications.

The arguments are divided into *predicate arguments* and *non-predicate
arguments*.  Predicate arguments determine whether the route matches the
current request: all predicates must pass in order for the route to be chosen.
Non-predicate arguments do not affect whether the route matches.

name

    [Non-predicate] The first positional arg; required. This must be a unique
    name for the route. The name will be used to register a view for this route,
    and to generate URLs.

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
    in advanced cases to do traversal on the remainder of the URL.

factory

    [Non-predicate] A callable (or asset spec). This is used to define a
    route-specific context. In URL dispatch, this returns a
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

Models
======

This is where you define your domain model; i.e., what makes this application
different from other Pyramid applications. A good application structure
separates domain logic (not Pyramid-specific or UI-related) from view logic
(Pyramid-specific or UI-related). This makes it easy to use the domain code
outside of the web application (in standalone utilities) or to port it to
another framework (if you ever decide to do so).

*Note:* the term "model" is used in two different ways. Collectively it means
all your ORM classes and domain logic together. (One model per application.)
Individually it means a single ORM class. (Several models in one application.)
Either way is fine, but beware that the word "model" (singular) can mean one or
the other. This led to a controversy in both Pylons and Pyramid on whether to
put "model" or "models" in the scaffolds. Pylons chose "model"; Pyramid chose
"models". But it doesn't matter, and you can rename models.py to model.py if
you wish. Just be aware that the word "model" can mean either one class or all
classes together.

At minimum you should define your database tables and ORM classes here. Some
people also put other business logic here, either as methods in the ORM classes
or as functions. Other people put miscellaneous domain logic into a 'lib'
package (*zzz/lib*). Others put the entire models and domain logic in a
separate Python distribution, which they import into the Pyramid application.
Others put domain logic directly into the views, but this is not recommended
unless it's a small amount of code because it mixes framework-independent and
framework-dependent code. 

The default *zzz/models.py* looks like this::

    from sqlalchemy import (
        Column,
        Integer,
        Text,
        )

    from sqlalchemy.ext.declarative import declarative_base

    from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
        )

    from zope.sqlalchemy import ZopeTransactionExtension

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    Base = declarative_base()

    class MyModel(Base):
        __tablename__ = 'models'
        id = Column(Integer, primary_key=True)
        name = Column(Text, unique=True)
        value = Column(Integer)

        def __init__(self, name, value):
            self.name = name
            self.value = value

This is just one way to organize a SQLAlchemy model. All SQLAlchemy models
models will have a DBSession, declarative base, and ORM classes unless you're
doing something unusual like not using the object-relational mapper or not
using the declararive syntax. But different people have different ideas about
what to name the variables or where to put them. We'll see an alternative
structure later. If you're unfamiliar with SQLAlchemy, the `SQLAlchemy manual`_
is well written and informative.


Views
=============

A Pyramid view is equivalent to a Pylons controller action: it's the
page-specific routine where the request is processed and an HTML response is
generated. The default *zzz.views* module looks like this::

    from pyramid.view import view_config

    from .models import (
        DBSession,
        MyModel,
        )

    @view_config(route_name='home', renderer='templates/mytemplate.pt')
    def my_view(request):
        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
        return {'one':one, 'project':'Zzz'}

A view can be either a function or a method, and it can be located anywhere.
You must register each view with the configurator, either by calling
``config.add_view()`` or -- as in this example -- by using the ``@view_config``
decorator in conjunction with ``config.scan()``. The scan method imports the
application's modules recursively, and registers all callables decorated with
``@view_config``.

Pylons is more specific about actions. An action must be a method in a
controller class, the class must inherit from a compatible base class, and the
class must be located in a module determined by the class's name. The action
may take arguments corresponding to routing variables, and it normally ends
with "return render(TEMPLATE_NAME)", which renders an HTML string. Magic global
variables contain the current request, response, session, cache, application
globals, and a URL generator.

A Pyramid view *function* takes a ``Request`` and returns a ``Response``. But
if the ``@view_config`` has a ``renderer=`` argument, it returns a dict of
template variables instead. The renderer invokes the specified template with
the variables, and generates the ``Response``. This is similar to TurboGears. 
It has advantages in unit testing and with alternate output formats (such as
JSON). That's because ``@view_config`` *does not change the function's arguments
or return value*. It merely sets function attributes which affect how the view
is registered. So a unit test that calls the view function directly gets back
the dict of variables, not a HTML string.

In the example, the ``renderer=`` arg names a template. Because the filename
ends in ".pt", Pyramid recognizes it as a Chameleon template and invokes the
Chameleon renderer. The renderer fills the template with the variables and
generates a ``Response``. A Mako renderer is also available, and non-template
renderers for JSON and other formats. The view's return value is whatever type
the renderer accepts. Template renderers normally accept dicts, while
non-template renderers may accept other types.

A view *method* is like a view function, except that the ``request`` argument is 
passed to the class's constructor rather than to the method. So a view class is
normally defined like this::

    class MyViewClass(object):
        def __init__(self, request):
            self.request = request

        @view_config(route_name='home', renderer='templates/mytemplate.pt')
        def my_view(self):
            # req = self.request
            one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
            return {'one':one, 'project':'Zzz'}

Later we'll see a ``Handler`` base class that takes this a step further. 

The ``route_name=`` argument to ``@view_config`` tells which route to attach
this view to. It's a required argument when using URL dispatch. Several
optional arguments are available to specify a permission the user must have to
invoke the view, and what kinds of requests the view matches (this is to limit
the view to certain HTTP methods, certain routing variable values, certain
query parameter values, 

optional arguments:

permission

    A string naming a permission that the current user must have in order to
    invoke the view.

http_cache

    Affects the 'Expires' and 'Cache-Control' HTTP headers in the response.
    This tells the browser whether to cache the response and for how long.
    The value may be an integer specifying the number of seconds to cache,
    a ``datetime.timedelta`` instance, or zero to prevent caching. This is
    equivalent to calling ``request.response.cache_expires(value)`` within the
    view code.




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
    :noindex:

    Render a template and return a string. 'renderer_name' is a template
    filename or renderer name. 'value' is a dict of template variables.
    'request' is the request, which is needed only if the template cares
    about it.

    If the function can't find the template, try passing "zzz:templates/"
    as the ``package`` arg.

.. function:: pyramid.renderers.render_to_response(renderer_name, value, request=None, package=None)
    :noindex:

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
can raise them, Pyramid prefers that you return them instead. If you intend to
raise them, you have to define an exception view that receives the exception
argument and returns it, as shown in the Views chapter in the Pyramid manual.
(On Python 2.4, you also have to call the instance's ``.exception()`` method
and raise that, because you can't raise instances of new-style classes in 2.4.) 
A future version of Pyramid may have an exception view built-in; this would
conflict with your exception view so you'd need to delete it, but there's no
need to worry about that until/if it actually happens.

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
   :noindex:

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
   :noindex:

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
   :noindex:

   Create a route connecting a URL pattern directly to a view callable outside
   a handler.  The view is specified with a 'view' arg. If the view is a
   function, it must take a Request argument and return a Response (or any
   object with the three required attributes). If it's a class, the constructor
   takes the Request argument and the specified method (``.__call__`` by
   default) is called with no arguments.

.. method:: config.add_view(\*\*kw)
   :noindex:

   I register a view (specified with a 'view' arg). In URL dispatch, you
   normally don't call this directly but let ``config.add_handler`` or
   ``config.add_route`` call it for you. In traversal, you call this to
   register a view. The 'name' argument is the view name, which is used by
   traversal to choose which view to invoke.

Two others you should know about:

.. function:: config.scan(package=None)
   :noindex:

   I scan the specified package (which may be an asset spec) and import all its
   modules recursively, looking for functions decorated with ``@view_config``.
   For each such function, I call ``add_view`` passing the decorator's args to
   it. I can also scan a package, in which case all submodules in the package
   are recursively scanned. If no package is specified, I scan the caller's
   package (i.e., the entire application). 
   
   I can also be called for my side effect of importing all of a package's
   modules even if none of them contain ``@view_config``.

.. function:: @view_config(\*\*kw)
   :noindex:

   I decorate a function so that ``config.scan`` will recognize it as a view
   callable, and I also hold ``add_view`` arguments that ``config.scan`` will
   pick up and apply.  I can also decorate a class or a method in a class.


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
   :noindex:

   The current request.

.. attribute:: context
   :noindex:

   The context (same as ``request.context``).

.. attribute:: renderer_name
   :noindex:

   The fully-qualified renderer name; e.g., "zzz:templates/foo.mako".

.. attribute:: renderer_info
   :noindex:

   An object with attributes ``name``, ``package``, and ``type``.

The subscriber in your application adds the following additional variables:

.. attribute:: c, tmpl_context
   :noindex:

   ``request.tmpl_context``

.. attribute:: h
   :noindex:

   The helpers module, defined as "zzz.helpers". This is set by a subscriber
   callback in your application; it is not built into Pyramid. 

.. attribute:: session
   :noindex:

   ``request.session``.

.. attribute:: url
   :noindex:

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

WebHelpers 1.3 has some new URL generator classes to make it easier to use
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


.. _PasteDeploy manual: http://pythonpaste.org/deploy/
.. _MultiDict API: api.html#multidict
.. _API: api.html
.. _minimal application: http://docs.pylonsproject.org/projects/pyramid/en/1.2-branch/narr/firstapp.html
.. _asset syntax: http://docs.pylonsproject.org/projects/pyramid/en/1.2-branch/narr/assets.html#asset-specifications
.. _SQLAlchemy manual: http://www.sqlalchemy.org/docs/
