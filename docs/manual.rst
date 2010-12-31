Users Guide
===========

**pyramid_sqla** is a SQLAlchemy_ helper for Pyramid_ applications. It provides
a central database session and an engine registry, and manages
commits/rollbacks centrally like TurboGears does, using the repoze.tm2_
transaction middleware.  Unlike the Pylons 1 application template, there's no
"meta" module or "init_model()" function in the application's model. Instead,
the things that were in meta have been moved into the library itself. This
makes it easier to keep your model in a package without interdependencies
between the modules, because each module just imports the library.

.. _SQLAlchemy: http://sqlalchemy.org/
.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/
.. _zope.sqlalchemy: http://pypi.python.org/pypi/zope.sqlalchemy
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _repoze.tm2: http://docs.repoze.org/tm2/
.. _transaction: http://pypi.python.org/pypi/transaction

The library follows the philosophy of making simple things simple and complex
things possible.  Applications with a single database requires only a few lines
of configuration as shown in "Usage" below. Applications with multiple engines
requires some more configuration and decision-making as described under
"Multiple Engines". Reflected databases may be a more difficult issue; we think
they can be done with an "init_model()" function as discussed under "Reflected
Databases".

pyramid_sqla has five dependencies: Pyramid_, SQLAlchemy_, repoze.tm2_, and
zope.sqlalchemy_ (for ZopeTransactionExtension, required by repoze.tm2), and
transaction_.

Usage
-----

For a simple Pyramid application with one database engine, follow these steps:

1. Run:
   
   .. code-block:: sh

        $ paster create -t pyramid_sqla MyApp

   substituting your own application name. This will create a directory *MyApp*
   containing the application.

2. In *MyApp/development.ini* change the default database URL if necessary:

   .. code-block:: ini

        sqlalchemy.url = sqlite:///%(here)s/db.sqlite

   You can add any SQLALchemy engine options you need, such as:

   .. code-block:: ini

        sqlalchemy.pool_recycle = 3600
        sqlalchemy.convert_unicode = true

   The logging is configured to log SQL queries but not results. For less or
   more logging, adjust the "level" line in the "[logger_sqlalchemy]" section.
   Level "INFO" logs queries, "DEBUG" logs queries and results (verbose!), and 
   "WARN" logs neither one.

3. In models or views or wherever you need them, access the database session
   and engine this way::

        import pyramid_sqla

        Session = pyramid_sqla.get_dbsession()
        engine = pyramid_sqla.get_dbengine()

Note that ``get_dbsession()`` returns a SQLAlchemy `scoped session`_
not a plain SQLAlchemy session. Also, if ``init_dbsession`` configures a
default engine, it also binds ``Base.metadata`` to it.

See `model examples <model_examples.html>`_ for examples of model code, and 
`application templates <application_templates.html>`_ for a detailed
description of the differences between this application template and a basic
Pyramid template.

Managed transactions
--------------------

The scoped session is managed by the repoze.tm2 middleware using
ZopeTransactionSession.  On egress the middleware will commit the session
unless an uncaught exception occurs, in which case it will rollback the
session. You can explictly commit and rollback in your view like this::

    import transaction
    transaction.commit()
    # Or:
    transaction.abort()

This may be useful if you want to commit a lot of data a little bit at a time.

To prevent *any* database writes during this request, including any performed
by other parts of the application or middleware, call::

    transaction.doom()

The transaction manager also takes care of closing the dbsession at the end of
every request, to prevent potentially obsolete or unauthorized data from
leaking into the next request the thread handles.

If you don't want managed transactions at all, pass
``manage_transaction=False`` to ``init_dbsession``, and do *not* wrap your
application in the ``repoze.tm2`` middleware. In this case you must call
``dbsession.commit()`` yourself or your changes will be lost. And you may even
get a SQLAlchemy exception if you don't call either ``dbsession.commit()`` or
``dbsession.abort()`` in a timely manner. (This occurs especially when the
database itself raises an error such as duplicate primary key. This may be
reported to use as ``sqlalchemy.OperationalError``. When this occurs it leaves
the dbsession in an invalid state and you must call ``dbsession.abort()`` or
you'll get another exception when you run another query.) To enable autocommit,
pass a sessionmaker arg like this::

    pyramid_sqla.init_dbsession(..., manage_transaction=False,
        sessionmaker_args={"autocommit": False})


Initialiazing the database
--------------------------

Reflected tables
----------------

Reflected tables pose a bit of a dilemma because it depends on a live database
engine but that may not available when the module is imported. There are two
ways around this. One way is to assume that when the module is imported,
``pyrmaid_sqla.init_dbsession()`` has already been initialized, and thus that
``get_dbengine()``, ``get_dbsession()``, and ``Base`` have all been bound to
the appropriate engine. The other way is to put an ``init_model()`` function in
your model, and call it after the engine has been configured. The function
would then do everything that depends on a live engine. You can either pass the
engine to the function or have the function call ``get_dbengine()`` to fetch
it.

When using ``init_model()`` with declarative, we think you'd have to put the
entire declarative class inside the function and use a ``global`` statement to
assign it to the module scope. When not using declarative, we think you can put
the ORM class at the module level, but the table definition and mapper would
have to be inside the function, again using ``global`` to put the table at the
module level.

If you choose not to use ``init_model()``, remember to initialize
``pyramid_sqla`` before importing the models. The application template
initializes the database in *myapp/__init__.py*, and does not import the models
except in views and in *websetup.py*. (Actually, it doesn't import the models
at all, but this is where you most likely would.)

Multiple databases
------------------

If you need to connect to multiple databases, list them all in
*development.ini* under distinct prefixes. For instance:

.. code-block: ini

    sqlalchemy.url = postgresql://me:PASSWORD@localhost/mydb
    stats.url = mysql://account:PASSWORD@example.com/stats

Or:

.. code-block: ini

    data.url = postgresql://me:PASSWORD@localhost/mydb
    sessions.url = sqlite:///%(here)s/scratch.sqlite

Then modify *myapp/__init__.py* and replace the ``pyramid_sqla.init_dbsession``
call. What to replace it with depends on what you want to do. Let's assume that
if the application has a default engine, it's called "default" and corresponds
to an INI prefix "sqlalchemy.". If there are two other (non-default) engines,
they will be called "engine1" and "engine2" as both their engine name and INI
prefix.

A default engine plus other engines
+++++++++++++++++++++++++++++++++++

In this scenario, the default engine is used for most operations, but two other
engines are also used occasionally::

    # Initialize the default engine.
    pyramid_sqla.init_dbsession(settings, prefix="sqlalchemy.")

    # Initialize the other engines.
    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")

Queries will choose the default engine by default. To choose a different engine
you have to use the ``bind=`` argument on some methods, or 
``engine.execute(sql)`` to run a SQL SELECT or command on a particular engine.

Two engines, but no default engine
++++++++++++++++++++++++++++++++++

In this scenario, two engines are equally important, and neither is predominent
enough to deserve being the default engine. This is useful in applications
whose main job is to copy data from one database to another. ::

    pyramid_sqla.init_dbsession()
    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")

Because there is no default engine, queries will fail unless you specify an
engine every time using the ``bind=`` argument or ``engine.execute(sql)``.

Different tables bound to different engines
+++++++++++++++++++++++++++++++++++++++++++

It's possible to bind different ORM classes to different engines in the same
database session, but ``init_dbsession()`` has no built-in support for it. 
Instead you should configure your application with no default engine, and
then call the scoped session's ``.configure`` method with the ``binds=``
argument to specify which classes go to which engines. For instance::

    dbsession = pyramid_sqla.init_dbsession()
    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")
    import myapp.models as models
    binds = {models.Person: engine1, models.Score: engine2}
    dbsession.configure(binds=binds)

The keys in the ``binds`` dict can be SQLAlchemy ORM classes, table objects, or
mapper objects.

API
---

.. currentmodule:: pyramid_sqla

.. automodule:: pyramid_sqla

.. autofunction:: init_dbsession

.. autofunction:: add_engine

.. autofunction:: get_dbsession

.. autofunction:: get_engine

.. autofunction:: get_base
