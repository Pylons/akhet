Migrating a Pylons Application to Akhet
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

XXX Pasted from a mailing list message; reformat.

> I've been developing a Pylons application over the past year or so.
> The functionality has been implemented using examples from the Pylons
> book. The application has over 20 controllers with more than six
> functions each and makes use of:
> "Pylons>=1.0",
> "SQLAlchemy>=0.5,<=0.5.99",
> "Mako",
> "WebHelpers>=1.0",
> "FormBuild>=3.0,<=3.99",
> "AuthKit>=0.4.3,<=0.4.99",
>
> Having read your migration guide I find it hard to understand what the
> most effective way of porting my application to Pyramid would be.
> Should I start changing things in my exisitng project? What changes do
> I need to make? Or would it be more productive to start a project from
> fresh using the paster pyramid_sqla template and copy and paste
> functionality from my Pylons project?
>
> A tutorial describing how to port a simple Pylons project to Pyramid
> would be very much appreciated.

I haven't done this myself yet, but here's how I think I'd approach it
based on previous upgrading from Pylons 0.9.7 to Pylons 1, and
creating a new application because the environments are so different.

I'd make only one change in your existing project: bring it up to
SQLAlchemy 0.6.  That way you'll be in your familiar environment and
it will be easier to debug anything. I can't remember why SQLAlchemy
was pinned below 0.6, but I guess if you remove that restriction and
upgrade you'll find out why if it affects you. It may just be because
0.6 issues warnings if you put non-unicode string literals into
unicode fields. If you have any problems you can't figure out from the
SQLAlchemy 0.6 migration guide, you can ask them here.

Then I'd create a new Pyramid project using pyramid_sqla (or akhet if
it's released by then) and start porting parts of the application bit
by bit.  The model may be the easiest to start with.

Then set up your site template if you're using one, empty out the
index template, make it inherit from the site template, and put in
some dummy content to make sure it works. Then you can port the home
page if it's simple enough, or make a dummy home page with some basic
links to your other pages.

Then start porting the handlers one at a time, copying over the
templates and helpers and stuff as you need them.  The templates will
remain the same except ${c.foo} changes to ${foo} -- and make sure
that doesn't overlap with a local variable ('for' variable, argument,
'<% %>' variable, etc).

In the view method, path variable arguments change to
``self.request.matchdict['var']``. GET/POST variables remain the same.
The method returns a dict of template variables, and the ``@action``
decorator points to the template. Any state information you need
(which in Pylons would be in the special globals) is under
``self.request`` somewhere.

If you have variables in your site template, these can remain 'c'
variables. In your handler's __init__function (or rather in a common
base class), put ``c = self.request.tmpl_context``, and assign the
variables.

If you have your own ``app_globals`` attribtues, migrate these to the
``settings`` dict if feasable. You can set these in the application's
main() function, and retrieve them as
``self.request.registry.settings`` I think it's called.

When you have a handler ready, you'll have to make a route to it.
(Actually, I define all my routes before I define my views, so you
could do that too. But you may have to comment out the ones pointing
to nonexistent handlers if you get any errors.)

For URL generation, pyramid_sqla has a slight annoyance that's fixed
in Akhet-dev. ``url`` in templates is aliased to the ``route_url``
function, which doesn't know about the request, so you have to pass
the request in every call. In Akhet, ``url`` is aliased to a
URLGenerator which knows about the request and context. Calling it is
the same as ``request.route_url``, and it has other methods
corresponding to the other generation functions. It's available in
views as ``self.request.url_generator``. The author says it's been
tested but I haven't tested it yet, so it may have some initial bugs.

Generating static URLs is trickier, as is described in the migration guide.
https://bytebucket.org/sluggo/pyramid-docs/wiki/html/migration.html#static-files
The way pyramid_sqla and Akhet handle static files, while it's the
closest to Pylons, doesn't provide any way to generate URLs to them.
You can simply join the relative URL to ``request.application_path`` I
think it's called (which would normally be a slash), or hardcode the
URL.

Otherwise, you can switch to Pyramid's add_static_view and then
everything will be under the "/static" URL prefix. Then you can
generate URLs to them using ``url.static()``. But this won't work for
top-level URLs like "/robots.txt", "/favicon.ico" or those under
another prefix like "/images". You'd have to create custom views for
those.

For forms, you can try sticking with FormBuild or switch to Deform or
one of the other libraries. I don't know whether FormBuild is
compatible with Pyramid, and I'm not sure how well maintained it is.
Deform was written by chrism who wrote Pyramid, so it has good
support. I want to make a form-comparison demo so I can decide myself
which library I want to use.

For auth, I would port your scheme to Pyramid's built-in auth if
feasable, because that will have better long-term support. I believe
AuthKit's author (the same who wrote FormBuild and the Pylons book)
has stopped recommending it. If you have a complex permissions system,
you'll have to decide whether the time it takes to port it is worth
the better support you'll get. If you need authentication mechanisms
that the built-in auth doesn't have, you might find them in
repoze.who, but then you'll have to integrate the two.

That's all I can think of off the top of my head. Others may have
different advice. If you have specific questions about the best way to
port certain constructs, do ask about it because it may be a missing
FAQ or a hole in the docs, or something we just haven't considered
yet.

