URL generator
%%%%%%%%%%%%%

A class that consolidates the various URL-generating functions in Pyramid into
one concise API that's convenient for templates. It performs the same job as
``pylons.url`` in Pylons applications, but the API is different.

Pyramid has several URL-generation routines but they're scattered between
Pyramid request methods, WebOb request methods, Pyramid request attributes,
WebOb request attributes, and Pyramid functions. They're named inconsistently,
and the names are too long to put repeatedly in templates.  The methods are
usually, but not always, paired: one method returning the URL path only
("/help"), the other returning the absolute URL ("http://example.com/help").
Pylons defaults to URL paths, while Pyramid tends to absolute URLs (because
that's what the methods with "url" in their names return).  The Akhet author
prefers path URLs because the automatically adjust under reverse proxies, where
the application has the wrong notion of what its visible scheme/host/port is,
but the browser knows which scheme/host/port it requested the page on. 

URLGenerator unifies all these by giving short one-word names to the most
common methods, and having a switchable default between path URLs and absolute
URLs.

Usage
=====

Copy the "subscribers" module in the Akhet demo app (*akhet_demo/subscribers.py*)
to your own application, and modify if desired. Then, include it in your main
function::

    # In main().
    config.include(".subscribers")

The subscribers attach the URL generator to the request as ``request.u``, and
put it in the template namespace as ``u``. Both names are short and sweet,
conserving horizontal space in templates and views, giving you more space to
specify the arguments.

URLGenerator was contributed by Michael Merickel and modified by Mike Orr.

API
===

.. autoclass:: akhet.urlgenerator.URLGenerator
   :members: __init__, app, ctx, route, current, resource
   :undoc-members:

   .. method:: __call__(\*elements, \*\*kw)

      Same as the ``.route`` method.


Subclassing
===========

The source code (*akhet/urlgenerator.py*) has some commented examples of things
you can do in a subclass. For instance, you can make a method to generate a URL
to a static asset in your application, or a static asset in Deform or
another third-party package, letting the method fill in parts of the asset
spec. The instance has ``request`` and ``context`` attributes, which you can
use to calculate any URL you wish. You can put a subclass in your application
and then adjust the subscribers to use it.

.. include:: ../links.rst
