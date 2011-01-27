Usage and API
%%%%%%%%%%%%%

The ``pyramid_sqla`` package contains three things: a SQLAlchemy scoped
session, a place for registering SQLAlchemy engines by name, and a declarative
base object. You can use all of these together in your application, or just use
some of them and ignore the others, as you prefer.

Installation
============

Install pyramid_sqla like any Python package, using either "pip install
pyramid_sqla" or "easy_install pyramid_sqla". To check out the development
repository: "hg clone http://bitbucket.org/sluggo/pyramid_sqla". 

Usage
=====

1. Create an application:
   
   .. code-block:: sh

        $ paster create -t pyramid_sqla MyApp

   It should work out of the box:

   .. code-block:: sh

        $ cd MyApp
        $ python setup.py egg_info
        $ paster serve development.ini

   The default application doesn't define any tables or models so it doesn't
   actually do anything except display some help links.

2. In *development.ini* change the default database URL to your database:

   .. code-block:: ini

        sqlalchemy.url = sqlite:///%(here)s/db.sqlite

   The default creates a SQLite database in the application directory. If
   you're using SQLite, you'll have to install it. (If you're still using
   Python 2.4, you'll also have to install the ``pysqlite`` package.)

   You can add other SQLALchemy engine options such as:

   .. code-block:: ini

        sqlalchemy.pool_recycle = 3600
        sqlalchemy.convert_unicode = true

   Engine options are listed under `Engine Configuration`_ in the SQLAlchemy
   manual, and in the Dialects_ section for particular databases.

3. If you want your engine to always convert String and Text columns to unicode
   regardless of what the INI file says, edit *myapp/__init__.py* and change
   the line::

        pyramid_sqla.add_engine(settings, prefix="sqlalchemy.")

   to::

        pyramid_sqla.add_engine(settings, prefix="sqlalchemy.", 
            convert_unicode=True)

3. In models or views or wherever you need them, access the database session,
   engine, and declarative base this way::

        import pyramid_sqla

        Session = pyramid_sqla.get_session()
        engine = pyramid_sqla.get_dbengine()
        Base = pyramid_sqla.get_base()

   Note that ``get_session()`` returns a SQLAlchemy `scoped session`_.
   This is traditionally assigned to ``Session`` with a capital S to remind us
   it's not a plain session. (Don't confuse SQLAlchmey sessions with HTTP
   sessions, which are completely different things.)

4. If the application needs to create the database and add initial data,
   customize *myapp/scripts/create_db.py* and run it:

   .. code-block:: sh
        
        $ python -m myapp.scripts.create_db development.ini


See `model examples <model_examples.html>`_ for examples of model code, and 
`application templates <application_templates.html>`_ for a detailed
description of the differences between this application template and a basic
Pyramid template.


API
===

.. currentmodule:: pyramid_sqla

.. automodule:: pyramid_sqla

.. autofunction:: add_engine

.. autofunction:: get_session

.. autofunction:: get_engine

.. autofunction:: get_base

.. autofunction:: reset

.. autofunction:: includeme

(``.add_static_route`` is explained on the Non-Database Features page.)

Managed transactions
====================

``pyramid_sqla`` has managed transactions. After the view is called, it will
automatically commit all database changes unless an uncaught exception occurs,
in which case it will roll back the changes. It will also clear the Session for
the next request.

You can still commit and roll back explicitly in your view, but you'll have to
use the ``transaction`` module instead of calling the Session methods
directly::

    import transaction
    transaction.commit()
    # Or:
    transaction.abort()

You may want to do this if you want to commit a lot of data a little bit at a
time.

You can also poison the transaction to prevent *any* database writes during this
request, including those performed by other parts of the application or
middleware. To do this, call::

    transaction.doom()

Of course, this doesn't affect changes that have already been committed.

The implementation is a combination of three packages that work together.
``transaction`` is a generic transaction manager. ``zope.sqlalchemy`` applies
this to SQLAlchemy by exposing a ``ZopeTransactionExtension``, which is a
SQLAlchemy session extension (a class that enhances the session's behavior).
The ``repoze.tm2`` middleware takes care of the commit or rollback at the end
of the request processing.

Starting with ``pyramid_sqla`` 1.0rc1 and ``repoze.tm2`` 1.0b1, the transaction
will also be rolled back if the application returns a 4xx or 5xx status, or if
the response header 'X-TM-Abort' is present. This is done by a "commit veto"
callback in ``repoze.tm2``. You can customize the veto criteria by overriding
the callback function in development.ini; see `Using a Commit Veto`_ for an
example.



Disabling the transaction manager
---------------------------------

If you don't want managed transactions, reconfigure the Session to not have the
extension::

    Session.config(extension=None)

and also delete the "egg:repoze.tm2#tm" line in the "[pipeline:main]" section
in *development.ini*.  If you disable the manager, you'll have to call
``Session.commit()`` or ``Session.rollback()`` yourself in your views. You'll
also have to configure the application to remove the session at the end of the
request. This would be in an event subscriber but I'm not sure which one.

Caveat: adding your own session extensions
------------------------------------------

If you modify the ``extension`` session option in any way you'll lose the
transaction extension unless you re-add it. The extension lives in the
semi-private ``_zte`` variable in the library. Here's how to add your own
extension while keeping the transaction extension::

    Session.configure(extension=[MyWonderfulExtension(), pyramid_sqla._zte])

Bypassing the transaction manager without disabling it
------------------------------------------------------

In special circumstances you may want to do a particular database write while
allowing the transaction manager to roll back all other writes. For instance,
if you have a separate access log database and you want to log all responses,
even failures. In that case you can create a second SQLAlchemy session using
``sqlalchemy.orm.sessionmaker`` -- one that does *not* use the transaction
extension -- and use that session with that engine to insert and commit the log
record. 
 

Multiple databases
==================

The default configuration in *myapp/__init__.py* configures one database::

    import pyramid_sqla as psa
    psa.add_engine(settings, prefix="sqlalchemy.")

To connect to multiple databases, list them all in
*development.ini* under distinct prefixes. For instance:

.. code-block: ini

    sqlalchemy.url = postgresql://me:PASSWORD@localhost/mydb
    stats.url = mysql://account:PASSWORD@example.com/stats

Or:

.. code-block: ini

    data.url = postgresql://me:PASSWORD@localhost/mydb
    sessions.url = sqlite:///%(here)s/scratch.sqlite

Then modify *myapp/__init__.py* and put an ``add_engine()`` call for each
database. The examples below elaborate on the API docs.

A default engine plus other engines
-----------------------------------

In this scenario, the default engine is used for most operations, but two other
engines are also used occasionally::

    # Initialize the default engine.
    pyramid_sqla.add_engine(settings, prefix="sqlalchemy.")

    # Initialize the other engines.
    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")

Queries will use the default engine by default. To use a different engine
you have to use the ``bind=`` argument the method that executes the query, 
``engine.execute(sql)`` to run a SQL SELECT or command in a particular engine.

Two engines, but no default engine
----------------------------------

In this scenario, two engines are equally important, and neither is predominent
enough to deserve being the default engine. This is useful in applications
whose main job is to copy data from one database to another. ::

    pyramid_sqla.init_dbsession()
    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")

Because there is no default engine, queries will fail unless you specify an
engine every time using the ``bind=`` argument or ``engine.execute(sql)``.

Different tables bound to different engines
-------------------------------------------

It's possible to bind different ORM classes to different engines in the same
database session.  Configure your application with no default engine, and then
call the Session's ``.configure`` method with the ``binds=`` argument to
specify which classes go to which engines. For instance::

    pyramid_sqla.add_engine(settings, name="engine1", prefix="engine1.")
    pyramid_sqla.add_engine(settings, name="engine2", prefix="engine2.")
    Session = pyramid_sqla.get_dbsession()
    import myapp.models as models
    binds = {models.Person: engine1, models.Score: engine2}
    Session.configure(binds=binds)

The keys in the ``binds`` dict can be SQLAlchemy ORM classes, table objects, or
mapper objects.


Logging
=======

The default application template is configured to log SQL queries.  To change
this, adjust the "level" line in the "[logger_sqlalchemy]" section. ::

     [logger_sqlalchemy]
     level = INFO
     handlers =
     qualname = sqlalchemy.engine
     # "level = INFO" logs SQL queries.
     # "level = DEBUG" logs SQL queries and results.
     # "level = WARN" logs neither.  (Recommended for production systems.)

SQLAlchemy has many other loggers; e.g., to show connection pool activity or
ORM operations. For details see `Configuring Logging`_ in the SQLAlchemy
manual.

*Caution:* Don't set the 'echo' engine option (i.e., don't do
"sqlalchemy.echo = true"). This sets up a duplicate logger which may cause
double logging.


Declarative base
================

The library includes a declarative base for convenience, but some people may
choose to define their own declarative base in their model instead. And there's
one case where you *have* to create your own declarative base; namely, if you
want to modify its constructor args. The ``cls`` argument is the most common:
it specifies a superclass which all ORM object should inherit. This allows you
to define class methods and other methods which are available in all your ORM
classes.

Reflected tables
================

Reflected tables pose a dilemma because it depends on a live database
connection in order to be initialized. But the engine may not be configured yet
when the model is imported. ``pyramid_sqla`` does not address this issue
directly. Pylons 1 models traditionally have an ``init_model(engine)`` function
which performs any initialization that requires a live connection. Pyramid
applications typically do not need this function because the Session, engines,
and base are initialized in the ``pyramid_sqla`` library before the model is
imported. But in the case of reflection, you may need an ``init_model``
function.

When not using declarative, the ORM classes can be defined at module level in
the model, but the table definitions and mappers will have to be set up inside
the ``init_model`` function using a ``global`` statement to set the module
globals.

When using declarative, we *think* the entire ORM class must be defined inside
the function, again using a ``global`` statement to project the values into
the module scope. That's unfortunate but we can't think of a way around it.
If you can, please tell us.


.. _Engine Configuration: http://www.sqlalchemy.org/docs/core/engines.html
.. _Dialects: http://www.sqlalchemy.org/docs/dialects/index.html
.. _Configuring Logging: http://www.sqlalchemy.org/docs/core/engines.html#configuring-logging
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _Using a Commit Veto: http://docs.repoze.org/tm2/#using-a-commit-veto
