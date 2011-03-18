API
%%%

APIs for functions and classes in the ``akhet`` package.

Config include function
-----------------------

.. autofunction:: akhet.includeme

Static route
------------

.. autofunction:: akhet.static.add_static_route

URL generator
-------------

.. autoclass:: akhet.urlgenerator.URLGenerator
   :members:
   :undoc-members:

MultiDict
---------

MultiDict is defined in WebOb (``webobb.multidict.MultiDict``) but its
documentation is so sparse that we have written our own documentation here.
Pyramid's ``request.params``, ``request.GET`` and ``request.POST`` are
MultiDicts.

A MultiDict is like a regular dict except that each key can have multiple
values. This is necessary to represent query parameters and form variables,
which can be multiple. ``request.params``, ``request.GET`` and ``request.POST``
are MultiDicts.

.. class:: MultiDict(dic=None, \*\*kw)

   An ordered dict that can have multiple values for each key.
   All the regular dict methods are supported. "Ordered" means that
   ``.keys()`` will return the keys in the order they were defined.

   Like a regular dict, the constructor can be called with an existing dict,
   an iterable of key-value tuples, or keyword args representing the dict keys.
   If the combination of args contain duplicate keys, all the impled values
   will be added to the dict, the keyword args last.

   .. method:: add(key, value)

      Add the value to the dict, not overriding any previous values.

      Note: ``dic[key] = value`` will replace all existing values for the key.

    .. method:: getall(key)

       Return all values for the key as a list. The list will be empty if
       the key is not present in the dict.

       Note: ``dic[key]`` and ``dic.get(key)`` return one arbitrary value,
       the last value added for the key.

    .. method:: getone(key)

       Return exactly one value for the key. Raise ``KeyError`` if the key has
       zero values or more than one.

    .. method:: mixed()

       Return a dict whose values are single values if the key appears once in
       the MultiDict, or lists if the key appears multiple times.

    .. method:: dict_of_lists()

       Return a dict where each key is associated with a list of values.

    .. method:: extend(dic=None, \*\*kw)

       Add items to the MultiDict. The arguments are the same as the
       constructor's.

    .. classmethod:: view_list(lis)

       Create a dict that is a view on the given list

    .. classmethod:: from_fieldstorage(fs)

       Create a MultiDict from a ``cgi.FieldStorage`` instance

.. class:: UnicodeMultiDict(multi, encoding=None, errors="strict", decode_keys=False)

    A MultiDict subclass that decodes returned values to unicode on the
    fly. Decoding is not applied to assigned values.

    The key/value contents are assumed to be ``str``/``strs`` or
    ``str``/``FieldStorages`` (as is returned by the ``paste.request.parse_``
    functions).

    Can optionally also decode keys when the ``decode_keys`` argument is
    True.

    ``FieldStorage`` instances are cloned, and the clone's ``filename``
    variable is decoded. Its ``name`` variable is decoded when ``decode_keys``
    is enabled.

.. class:: NestedMultiDict(\*dicts)

   A MultiDict subclass that wraps several MultiDict objects, treating them
   as one large MultiDict. A NestedMultiDict is read-only, although the
   contained MultiDicts are not.

.. class:: TrackableMultiDict(dic=None, \*\*kw)

   This is a MultiDict that functions as an observable. It's used internally
   in WebOb where other parts of the API need to know when a GET or POST
   variable changes. 

   In addition to the regular MultiDict constructor args, you can pass
   ``__tracker`` (two leading underscores) which is a callback function, and
   ``__name`` which is the object's ``repr()`` name.

   The callback function is called with zero to three positional args:
   ``self``, ``key``, and ``value`` (although the callback can name them
   differently, but it should give default values to all of them). ``self`` is
   the MultiDict's self.  ``key`` is passed if the method deletes a particular
   key. ``value`` is passed if the method sets a particular key or adds an
   additional value to a key.

   The ``.copy`` method returns a regular MultiDict. The tracker is not
   propagated to it.

   There appears to be a bug in the source, that if you instantiate a
   TrackableMultiDuct without a tracker, it defaults to None and you'll get an
   exception when a routine tries to call it.

.. class:: NoVars(reason=None)

    This is an always-empty MultiDict. Adding an item item raises ``KeyError``. 
    It's used internally in WebOb to distinguish between dicts that happen to
    be empty vs dicts that must be empty; e.g., ``request.POST`` in a GET
    request.
