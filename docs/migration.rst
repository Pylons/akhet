Migrating a Pylons Application to Akhet
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

A user wrote to the "pylons-discuss" mailing list:

    I've been developing a Pylons application over the past year or so.
    The application has over 20 controllers with more than six
    functions each and makes use of:

    * Pylons>=1.0
    * SQLAlchemy>=0.5,<=0.5.99
    * Mako
    * WebHelpers>=1.0
    * FormBuild>=3.0,<=3.99
    * AuthKit>=0.4.3,<=0.4.99

    Having read your migration guide I find it hard to understand what the
    most effective way of porting my application to Pyramid would be.
    Should I start changing things in my exisitng project? What changes do
    I need to make? Or would it be more productive to start a project from
    fresh using the paster pyramid_sqla template and copy and paste
    functionality from my Pylons project?

The migration guide has become this manual, and pyramdid_sqla has become Akhet,
but the question is still relevant.

If this were my application, I'd make only one change to the existing project:
bring it up to SQLAlchemy 0.6. (Or 0.7 if it's out by the time you read this.)
That will be easiest to do in your familiar environment where it'll be easier
to debug anything that might go wrong. One issue when upgrading from 0.5: 0.6
issues a warning if you assign a non-Unicode string to a Unicode column (or if
you have 'convert_unicode=True' which treats all String columns into Unicode
columns). You'll either have to convert all your string literals or disable the
warning if it becomes annoying. On the other hand, 0.6 also leverages the
native Unicode support that exists in some database drivers; this makes it more
efficient on SQLite and PostgreSQL/``psycopg2`` at least.

Then I'd make a new project using the "akhet" skeleton, and start porting your
code to it. The differences between Pylons and Pyramid are so large that it's
not worth trying to upgrade the application in place. (Note: in this chapter I
don't distinguish between Akhet features and generic Pyramid features;
that's what the rest of this manual is about.)

After creating the application, delete everything in the static directory and
replace it with your files. Then copy your helpers to *zzz/lib/helpers.py*, add
any necessary imports to *setup.py*, and install the application. ("python
setup.py develop", "pip install -e .", or "pip install .") Installing the
application updates the *ZZZ.egg-info* metadata and installs the new
dependencies.

Then empty out *index.html* and replace it with some minimal content. If you're
using a site template, copy it now and make index.html inherit from it. There's
no routing yet so you'll have to use hardcoded URLs or comment out the
``${url(...)}`` calls. You've already migrated the helpers so any
``${h.foo()}`` calls should work. If the site template depends on ``c``
variables set in the base controller, put equivalent attributes in
``zzz.handlers.base.Base.__init__`` under ``self.request.tmpl_context``.
(This object is available in template as both ``tmpl_context`` and ``c``, as in
Pylons.) Then run the application and make sure the home page works.

Then I'd work on the model, which probably has few if any dependencies on the
rest of the application. You should be able to copy your tables and classes
unchanged, and make them use the ``Session`` retrieved from SQLAHelper. You
won't need ``init_model`` unless you're using reflection; if you are, add a
call to it in the main function.

Copy your existing database, adjust *development.ini* for it, and empty out the
*index.html* template. Change the index view method to perform a simple model
lookup, pass the record to the template in the view's return dict, and make the
template display it. Run the application to make sure it works.

Now you can start porting your controllers to view handlers one at a time,
copying the templates as you need them.  The templates will remain the same
except ${c.foo} changes to ${foo} -- and make sure that doesn't overlap with a
local template variable (a 'for' variable, 'def' argument, '<% %>' variable,
etc).

In the view method, path variable arguments change to
``self.request.matchdict['var']``. GET/POST variables remain the same:
``self.request.params`` (or ``self.request.GET`` and ``self.request.POST``).
Instead of setting ``c`` variables, return a dict of template variables, and
set the ``@action`` decorator with the 'renderer' arg pointing to the template.

You *can* set ``c`` variables in the view for the template, assigning them to
``self.request.tmpl_context``, but this is unusual in Pyramid views. It's still
useful, however, to share data between the base class's .__init__ method, the
template, the view, and utility methods the view calls).

Any state information you need (which in Pylons would be in the special
globals) is under ``self.request`` somewhere.

If you have your own ``app_globals`` attribtues, migrate these to the
``settings`` dict if feasable. You can set these in the application's
main() function, and retrieve them as
``self.request.registry.settings`` I think it's called.

As in Pylons, the view handler is instantiated for each request, so any
``self`` attributes you set will be visible only in the current request.

When you've finished your handler, you'll have to make a route to it.
(Actually, I create applications by first writing down the URL structure, then
defining my routes and then my views. But in that case you'd have to comment
out routes pointing to views that don't exist yet.) In the default Akhet
application, routes are defined in an ``includeme`` function in
*zzz/handlers/__init__.py*, which is included in the main function via a 
``config.include()`` call.

As in Pylons, you can make a separate route for each view (with 'action' as a
keyword argument), or a general route for the entire handler (with "{action}"
as a path variable). You can't make a single route to multiple handlers; so
there's no equivalent to Pylons' "/{controller}/{action}" route.

Once the routes are defined, generating URLs is similar to Pylons. Call
``${url("route_name", arg1="value1")}``. To generate a URL based on the current
request's route, call ``${url.current(arg1="value1")}``. Unlike Pylons, these
methods do not convert keyword args not corresponding to path variables into
query parameters. Instead, pass a dict of query params via the '_query'
argument. (To propagate the current request's params, '_query=request.GET'.)
You can also pass '_anchor', which will be the page's "#anchor" value.
'_app_url' replaces the "scheme://host" prefix *if the URL generator was
configured to produce absolute URLs*. (It's not by default; see the `Templates
<architecture.html#templates>`_ section and `API <api.html>` page for details.)

If you want to create a link to the current URL with different query
parameters, see ``webhelpers.util.update_params`` in the WebHelpers package.
The current URL is ``${request.path}`` (path only without query),
``${request.path_url}`` (absolute without query), and ``${request.url}``
(absolute with query).

Making URLs to static files is trickier because the methods above won't
work for that. ``${url.app}`` is the application's base URL, so you can do
``${url.app}/subdir/filename.css`` to semi-hardcode the URL. (XXX Check if
url.app ends with a slash.)

Or you can switch to Pyramid's default way of serving static files
(add_static_view), which exposes the "/static" prefix to the user. Then you can
use ``${request.static_url()}``, and even set it up to generate external URLs
to a static media server. But this won't work for top-level URLs
("/favicon.ico"). URLGenerator does not have a shadow method for static_url;
there's a commented method in the source but we're not sure of the best API.
You can define a method in a subclass and use it in *subscribers.py*. There's
also a commented method to serve static files from the Deform library if you're
using that.

Speaking of forms, you can try sticking with FormBuild or switch to Deform or
one of the other libraries. I don't know whether FormBuild is compatible with
Pyramid, and I'm not sure how well maintained it is.  Deform was written by
chrism who wrote Pyramid, so it has good support. The Pylons form standard
(FormEncode + WebHelpers) also works under Pyramid. The ``@validate`` decorator
does not exist in Pyramid; it was seen as flawed and not worth porting.
Most Akhet users use "pyramid_simpleform", an add-on package in PyPI that
provides a way to organize form invocation-validating-processing inside the
view method.

For auth, I would port your scheme to Pyramid's built-in auth if feasable,
because that will have better long-term support. I don't know whether AuthKit
is compatible with Pyramid, and I believe AuthKit's author has stopped
recommending it. If you have a complex permissions system, you'll have to
decide whether the time it takes to port it to Pyramid's auth system is worth
it. If you need authentication mechanisms that the built-in auth doesn't have,
you might find them in repoze.who, but then you'll have to integrate the two
(and we're still researching whether that is feasable). There's also
repoze.what, which offers an authorization system with a permission hierarchy,
but I don't see how it's any better than Pyramid's auth or AthKit.

If your application is using ``app_globals`` attributes, migrate them to
Pyramid's ``settings`` dict. You can set them at the top of the main function,
and access them in views as``self.request.registry.settings["my_setting"]``,
and in templates as ``request.registry.settings["my_setting"]``.

Beaker caching is initialized in the settings. To use the cache decorators, see
the following:

*  http://docs.pylonsproject.org/projects/pyramid_beaker/dev/#beaker-cache-region-support
* http://beaker.groovie.org/caching.html#cache-regions

Pyramid has no cache object akin to Pylons ``app_globals.cache``, but with the
decorators you don't really need it. If you want to use it anyway, you can
create a cache object by instantiating ``beaker.cache.CacheManager``.

If you're using the REST/Atom URL structure (Routes ``map.resource()`` and
"paster restcontroller"), there are no equivalent helpers in Pyramid at this
time. You can define your own routes, or explore Pyramid's traversal feature.
You can use route predicates to limit a route to a certain HTTP method. If
you're tunneling PUT and DELETE via POST using the "_method" query parameter
(as ``webhelpers.html.tags`` does), you can test the "_method" parameter
directly with a route predicate: 'request_param="_method=PUT"'.
