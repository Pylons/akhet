Pyramid Vocabulary
%%%%%%%%%%%%%%%%%%

This is a supplement to the Glossary_ in the Pyramid manual. It focuses on the
subset of terms critical for Akhet, and compares them to Pylons.


Router

    A Pyramid WSGI application, which is an instance of
    ``pyramid.router.Router``.  Equivalent to ``PylonsApp``.

View (View Callable)

    A function or method equivalent to a Pylons controller action. It takes a
    ``Request`` object representing a web request, and returns a ``Response``
    object.  (The return value may be different when using a *renderer*.)

View Class (Handler)

    A class containing view methods, so equivalent to a Pylons controller.
    If the view is a method rather than a function, the ``request`` argument is
    passed to the class constructor rather than to the method. The
    ``pyramid_handlers`` package offers one Pylons-like way to define and
    register view classes.

MVC

    The Model-View-Controller pattern used in programming. Pyramid is more of a
    MV (Model-View) framework than MVC. Many contemporary web developers have
    given up on MVC as not being well suited to the web.  MVC envisions a
    three-way split between business logic, user interface, and framework
    interface, but in practice the latter two are hard to separate. A two-way
    split is more useful: the *model* which is all code specific to your
    business and can be used on its own, and the *view* which is all code
    specific to the framework, user interface, and HTTP/HTML environment.
    (The "controller" then is the framework itself.)

URL Dispatch

    A routing mechanism similar to Routes. It chooses a view for each incoming
    URL based on a set of rules.

Traversal

    Pyramid's other routing mechanism, which maps the URL's components to a
    recursive object-oriented data structure.  Traversal is an advanced topic;
    beginners are advised to stick to URL dispatch at first. Traversal is
    useful mainly in applications that allow users to define arbitrary URL
    subtrees, such as a content-management system (CMS) or a web-based file
    manager. URL dispatch, in contrast, works better when the URLs are known
    ahead of time or when they're a fixed depth (e.g., "/articles/{id}"). 

    If no route matches the URL, Pyramid tries traversal as a fallback. The
    data structure is null by default, so this is a no-op.

Context

    An object accessible to the view, which tells the "context" it was invoked
    in. This does not exist in Pylons. It's an additional piece of information
    distinct from the routing variables, query parameters, and other aspects of
    the request. It plays an important role in traversal, and in some advanced
    usages of URL dispatch.

Resource Tree, Root, Resource, Root Factory

    These are all used in traversal, and in some advanced usages of URL
    dispatch.

    A *resource tree* is the data structure that traversal maps the URL to.
    It's a recursive dict-like structure. The top-level node is called the
    *root*. A *root factory* is a callable that returns a *root*; i.e., the top
    node of a live resource tree.  The *resource tree* is most commonly a ZODB
    database, but it can also be implemented in SQL or on-the-fly (by a root
    object with a clever ``.__getitem__`` method that creates child nodes on
    demand). 

    If the request URL is "/a/b/c", traversal maps it to
    ``root["a"]["b"]["c"]``.  The final node (i.e., the value of the "c" key)
    is called the *resource*. That object is delivered to the view as the
    *context*.

    In URL dispatch, a *root factory* is normally not specified, and it
    defaults to a null factory which causes the *context* to be ``None``. 
    However, you can specify a custom *root factory* at either the top level or
    on an individual route. In this case, the factory should return a
    *resource* which will **be** the *context*.

Request

    An object which contains all state data pertinent to the current web
    request and the application runtime. It's a subclass of ``WebOb.Request``.
    Its attributes subsume the functionality of several Pylons globals
    (request, response, session, tmpl_context or c, url), the match dict, query
    parameters, etc. 

Response

    An object which specifies what kind of response to return to the user:
    the HTTP status, HTTP headers, and body content. It's normally a subclass
    of ``WebOb.Response`` but you can substite any object with the appropriate
    ``status``, ``headerlist``, and ``app_iter`` attributes.
    A view must return a Response unless it's using a renderer.

Renderer

    A function that takes a view's return value as input, and returns a
    Response.  Normally the view returns a dict of data values, and the
    renderer invokes a template to produce the Response body. Some renderers
    instead serialize the dict into another format such as JSON.

Event, Subscriber

    A mechanism for running arbitrary code at specific points during request
    processing or during the application's lifetime. You register *subscriber*
    callbacks for specific events, and Pyramid will call those callbacks when
    those events happen. The callback's arguments allow access to pertinent
    state data.

Asset Spec

    A fully qualified Python module name or object name, such as the strings
    "myapp.handlers" or "myapp.handlers:MyHandler". Many Pyramid methods
    accept these as arguments in lieu of the actual object. The colon separates
    the last item to import (a package or module) from the first item to fetch
    via attribute access (a variable in the module).
    
    Certain methods require an asset spec pointing to a non-Python file or
    directory inside a Python package. In this case, the right side of the
    colon is the relative path inside the package, using "/" delimeters
    regardless of platform. For instance, "myapp:static/" or
    "myapp.lib:images/logo.png".

Settings

    A dict of application configuration settings. This combines:
    
    * "deployment settings" parsed from the INI file (or passed in by
      whatever top-level script launches the application).
    * "application settings", or site-wide constants, set in the main function.
    * "application globals": data structures, non-SQLAlchemy database
      connections, a cache object, or other things that are global to all
      requests. These are also normally set in the main function.

Registry

    An object that is global to the application and contains internal framework
    data such as which routes and views have been defined. Application writers
    generally ignore it except when they need a setting, which are in its
    ``.settings`` attribute.


.. _Glossary: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html
