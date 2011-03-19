Pyramid Vocabulary
%%%%%%%%%%%%%%%%%%

Router

    A Pyramid WSGI application, an instance of ``pyramid.router.Router``.
    Equivalent to ``PylonsApp``.

View (View Callable)

    A function or method equivalent to a Pylons controller action. It takes a
    Request object representing a web request, and returns a Response object.
    (In Akhet the view's arguments and return value are different because of
    handlers and renderers.)

Handler (View Handler)

    A class containing view methods, so equivalent to a Pylons controller.
    Handlers are defined in the ``pyramid_handlers`` package and are
    documentated there.

MVC

    The Model-View-Controller pattern used in programming. Pyramid is more of a
    MV (Model-View) framework than MVC. Many contemporary web developers --
    while still supporting the basic principle of keeping your business
    logic separate from your user interface code -- have given up on the formal
    categories of MVC as not being well suited to the web.  MVC envisions a
    three-way split between business logic, user interface, and framework
    interface, but in practice the latter two are hard to separate. MVC was
    invented in the 1980s to separate application code from low-level
    keyboard drivers and video drivers, a situation not directly applicable to
    modern web development.

URL Dispatch

    A routing mechanism similar to Routes. It chooses a view for each incoming
    URL based on a set of rules.

Traversal

    Pyramid's other routing mechanism, which looks up a view and a context by
    matching the URL to a node in a resource tree.  Many Akhet applications do
    not use traversal, and the Akhet docs don't cover how to use it.
    Nevertheless, we'll briefly explain what it is.

    Traversal is especially suited to situations where URLs can be arbitrarily
    deep in ways that are unknown at application startup, such as a CMS system
    with an article at "/section/subsection/custom-sub-subsection/my-article".
    URL dispatch works only with URLs at a fixed depth, where specific
    variables correspond to known segments; e.g., "/articles/{id}".

    Traversal runs *after* all URL dispatch routes have been tried. It's
    possible in advanced usage to create a "hybrid" application where the left
    part of the URL corresponds to a route, and traversal is applied to the
    remainder of the URL.

Resource Tree, Root, Resource

    In traversal, a *resource tree* is a nested dict-like structure such as a
    ZODB database or a group of nested dicts. The outermost container object is
    the *root*. Each value in the nested dicts is a *resource*.

    In URL dispatch, the *root* can be any object. Normally you don't specify
    it, and the system provides a default root.

Context

    In traversal, the last resource traversed is the *context*. The context is
    available to the view as ``request.context``. The context acts as a second
    kind of model (separate from your "models" package), and it may also
    provide information for authorization.

    In URL dispatch, the context is normally the same as the root, an
    unimportant default object. However, you can override the context on a
    per-route basis to provide authorization information.

Request

    A subclass of WebOb.Request which contains all state data pertinent to the
    current request and the application runtime. Its attributes subsume the
    functionality of several Pylons globals (request, response, session,
    tmpl_context or c, url), the match dict, query parameters, etc. 

Response

    A subclass of WebOb.Response, or any object with the same ``status``,
    ``headerlist`` and ``app_iter`` attributes that a Response has.  
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
    generally ignore it except when they need a setting, which are in the
    ``.settings`` attribute.
