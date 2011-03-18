Unfinished Usage Doc Fragments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Cache
=====

For caching, you can configure Beaker caching the same way Pylons does, but this has not been currently documented. One users recommendation. Perhaps make a cache object in the registry or settings?
this should go away
pyramid_beaker has a cache setup method that ive written
and we should endorse the @cache_region decorator i think, this is the way ben wants beaker to be used afaik
OK. Can you write up a description so I don't get it wrong?
i would just link this instead http://docs.pylonsproject.org/projects/pyramid_beaker/dev/#beaker-cache-region-support
since it contains explanation how to configure it - and usage well - its covered in beaker docs - http://beaker.groovie.org/caching.html#cache-regions
i would just link those two sections instead
you can get caching up in 1 min with that
i even think it should be set up by akhet by default
athough chris seems allergic to beaker in general
I can put it into Akhet, but I need the exact code to put in. I'm not that familiar with caching, and if I read the links I might get a different interpretation than you intended.
ok
i can put it in
i think i added it to initial pyramid_sqla templates, before you started working on them
I do think Akhet should provide similar caching as Pylons, I just didn't know what to do.
Where would the cache object go? Some place under registry or registry.settiongs?
there is NO cache object ;-)
thats the fun
you dont need it
also there is cache manager
like pylons has
basicly when you use the decorator approach or region function - it checks beaker namespace for whatever regions are set up
in configuration phase
so in your app you can do
pyramid_beaker.set_cache_regions_from_settings(settings)
in main() when you configure your app
So app_globals.cache goes away?
and now @region_cache works eveywhere
yes
this is the "new best way" to use beaker i believe
What if you want to cache something directly rather than using the decorator?
i THINK you can just instantiate cache manager - and it should already read the data taht pyramid_beaker.set_cache_regions_from_settings(settings) - set up for it - but i would need to dig into the docs
to be 100% sure
or.. wait
give me a moment ill try to test it
i can see that most of beaker docs operate with decorator approach really
OK, so i did a test http://paste2.org/p/1303025
and it still works when i instantiated cache manager
i just dont think a lot of folks use cache manager - because basicly you STILL need to make a callable that you pass to it
tmpl_cache.get(key=2, createfunc=cache_me)
so why use this form when you can just decorate cache_me function in first place - its a lot more ellegant
OK, we'll just need to explain why it's missing and how to create it if you want it.

::

  
    @action(renderer='/default/index.jinja2', permission='__no_permission_required__')
    def index(self):
        from beaker.cache import CacheManager
        cache = CacheManager()
        tmpl_cache = cache.get_cache('lalala')
        print tmpl_cache.get(key=2, createfunc=cache_me)
        return {}

ok, ill have to ask ben what he really thinks about this approach, i wrote config method with his blessing, so i think it should be all good, but its best to ask him

Misc
====

file:///home/ergo/workspace/akhet/docs/_build/html/architecture.html#url-generation-methods - misses current_route_url - its important to have that one, otherwise url generation for paginate or grid will be big pain in the ass

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

    config.include('pyramid_sqla')

    # Set up routes and views
    config.add_handler('home', '/', 'pyramidapp.handlers:MainHandler',
                       action='index')
    config.add_handler('main', '/{action}', 'pyramidapp.handlers:MainHandler',
        path_info=r'/(?!favicon\.ico|robots\.txt|w3c)')
    config.add_static_route('pyramidapp', 'static', cache_max_age=3600)

The 'include' line creates the ``config.add_static_route`` method which we call
in the last line.

The first ``config.add_handler()`` call is an ordinary home page route, nothing
special about it. 

The second is a catchall route for "/{action}"; i.e., any one-component URL.
The ``path_info`` regex prevents the route from matching URLs referring to
top-level static assets. You'll have to do this with any routes that could
accidentally match your static URLs, which are generally routes with a variable
first component.

The ``config.add_static_route()`` call mounts the static directory onto "/" as
an overlay.
This method is defined as a function,
``pyramid_sqla.static.add_static_route()``. If you look at the source code, it
adds a route with a custom route predicate so that if the file doesn't exist, 
the route won't match the URL. This gives later routes or
traversal a chance to work, otherwise they would be blocked. If the file does
exist, the static view registered by this method will serve it.

(You can call the function directly if you wish, passing ``config`` as the
first argument. But it's more convenient to call it as a method.)

API
---

.. autofunction:: akhet.static.add_static_route

.. _w3c: http://www.w3.org/P3P/ 
