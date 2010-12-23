pyramid_sqla
============

**pyramid_sqla** is a SQLAlchemy_ helper for Pyramid applications. It provides
a central database session and an engine registry, and handles
commits/rollbacks centrally like TurboGears does, using the repoze.tm2_
transaction middleware.  Unlike the Pylons 1 application template, there's no
"meta" module or "init_model()" function in the application's model. Indeed,
there's hardly any boilerplate code in the model at all: just one import line.

.. _SQLAlchemy: http://sqlalchemy.org/
.. _ZopeTransactionExtension: http://pypi.python.org/pypi/zope.sqlalchemy
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _repoze.tm2: http://docs.repoze.org/tm2/

The library aims to make simple configurations simple and complex
configurations possible.  An application with a single database requires
only a few lines of configuration, as shown in "Usage" below. An application
with multiple engines requires some more configuration and decision-making, as
described under "Multiple Engines". Reflected databases may be a more difficult
issue; we tentatively think they can be done with an "init_model()" function,
as discussed under "Reflected Databases".

The library creates a SQLAlchemy `scoped session`_ (conventionally named
``Session`` with a capital S) using the ZopeTransactionExtension_ . This
extension, if combined with the repoze.tm2_ middleware, provides a central way 

Usage
=====

For a simple Pyramid application with one database engine, follow these steps:

1. Add it to your list of 'requires' dependencies in *setup.py*.

2. In your *development.ini* file add:

   .. code-block:: ini

        sqlalchemy.url = sqlite:///%(here)s/db.sqlite

   You can also add any SQLALchemy engine options such as:

    ..code-block:: ini

        sqlalchemy.pool_recycle = 3600
        sqlalchemy.convert_unicode = true

   To log SQL queries, modify the "[logger_sqlalchemy]" section in
   *development.ini*. Set ``level = INFO`` to log all
   queries, ``level = DEBUG`` to log queries and results (very verbose!),
   or ``level = WARN`` to log neither. If your *development.ini* does not have
   a "[logger_sqlalchemy]" section, create a new Pyramid application and
   copy all the logging sections from its *development.ini*.

2. In *myapp/__init__.py*, add the following at the top::

       import pyramid_sqla

   Then inside the ``main()`` function, add this like::

        pyramid_sqla.init_dbsession(settings, prefix="sqlalchemy.")

3. In models or views or anywhere else you need them::

    import pyramid_sqla

    Session = pyramid_sqla.get_dbsession()
    engine = pyramid_sqla.get_dbengine()

API
===

.. automodule:: pyramid_sqla

.. autofunction:: init_dbsession

.. autofunction:: get_dbsession

.. autofunction:: get_dbengine

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

