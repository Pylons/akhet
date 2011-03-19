Other Pyramid features
%%%%%%%%%%%%%%%%%%%%%%

Pyramid has several significant features that have no Pylons equivalent. These
are one of the reasons the Pylons developers decided to switch to the
repoze.BFG architecture (which is now Pyramid), so that we could leverage the
existing code rather than having to write it from scratch.

Events
======

The events framework provides hooks where you can insert your own code into the
request-processing sequence. It standardizes some features that were provided
ad hoc in Pylons or not at all. To use it, you write a callback function that
takes an ``event`` argument, and register it via ``config.add_subscriber()`` in
the main function.  Akhet applications have two predefined subscribers in
*zzz/subscribers.py* which can serve as examples.

The events are listed on the Pyramid `Events API`_ page. Each has a different
kind of ``event`` argument with different attributes.

    * ApplicationCreated: called by ``config.make_wsgi_app()`` when the
      application starts up. ``event.app`` is
      the application instance.

    * NewRequest: called at the beginning of each request, after the Request
      object is created. ``event.request`` is the request.

    * ContextFound: called later than NewRequest, after the router has found
      the context object through URL dispatch or traversal. Use this if you
      need both the request and the context.  ``event.request`` is the request,
      and ``event.request.context`` is the context.

    * NewResponse: called after a view or its renderer returns a Response.
      ``event.request`` is the request, and ``event.response`` is the response.

    * BeforeRender: called before rendering a template. ``event`` is a
      dict-like object containing the template's global variables. You can
      modify this dict to add new globals, but you'll get a ``KeyError`` if you
      try to set a key that already exists.

Each event type is a class in pyramid.events_ (e.g.,
``ApplicationCreated``). Each has a corresponding interface in
pyramid.interfaces_ (e.g., ``IApplicationCreated``). The class is what you pass
as the second argument to ``config.add_subscriber``. (You can also pass a
dotted string name: "pyramid.events.ApplicationCreated".) The interface
describes the API of the ``event`` object that's passed to your callback.

There are two other ways to modify or inspect responses, called "response
callbacks" and "finished callbacks".  These do not use the events
infrastructure. They're documented in the Hooks_ page in the Pyramid manual.
Unlike event subscribers, they have to be registered for each request. Note
that response callbacks are NOT called if certain exceptions occur. Finished
callbacks are always called, but they're called after the response has been
sent to the user so they can't influence it. 

The Pyramid manual says that NewResponse is not recommended and that middleware
is better for modifying the response, but what it actually means is that it may
be easier to write the equivalent functionality in middleware if you don't need
Pyramid-specific data. On the other hand, if you want to log the response and
certain request data in a database and you need Pyramid-specific data, an event
or callback is suitable because you know right where the data is, whereas in
middleware it may be difficult or impossible to get the data.

Extending applications
======================

Pyramid provides ways to let you or another developer *extend* an application
without touching its internal code. The second developer can create a separate
Pyramid application that references the first one, and adds or overrides
routes, views, templates, and static files. This allows the second developer to
add functionality to the application or change the way it looks or behaves. The
technique is described in the Extending_ chapter of the Pyramid manual.

However, Pyramid applications are not "pluggable" the way Django claims to be.
That is, you can't expect two arbitrary Pyramid applications written by
different people to fit together. Pyramid's flexibility makes this unfeasable.
The developers would have to agree on a common set of conventions for
structuring their applications, and write them with that in mind.


Request processing in detail
============================

The Pyramid manual has a step-by-step list of how it `processes a request`_,
from the time it's received from the webserver to the time the response is
given to the webserver. This is equivalent to the Pylons Execution Analysis,
although it doesn't cover Paste's and the WSGI server's roles.


.. _Events API: http://docs.pylonsproject.org/projects/pyramid/1.0/api/events.html#events-module
.. _pyramid.events: http://docs.pylonsproject.org/projects/pyramid/1.0/api/events.html#events-module
.. _pyramid.interfaces: http://docs.pylonsproject.org/projects/pyramid/1.0/api/interfaces.html#pyramid.interfaces.IApplicationCreated
.. _Hooks: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/hooks.html
.. _Extending: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/extending.html
.. _processes a request: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/router.html
