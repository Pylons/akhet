Usage and API
=============

Installation and demos
----------------------

Install pyramid_sqla like any Python package, using either "pip install
pyramid_sqla" or "easy_install pyramid_sqla". To check out the development
repository: "hg clone http://bitbucket.org/sluggo/pyramid_sqla". 

There's one demo application in the source distribution but it doesn't do much
yet. It displays your database URL. The create_db script puts a sample record
in a table. It has a pony and a unicorn (using Paste Pony). To run it, first
install pyramid_sqla, then do:

.. code-block:: sh
   :linenos:

    $ cd demos/SimpleDemo
    $ python setup.py egg_info
    $ python -m simpledemo.scripts.create_db development.ini
    $ paster serve development.ini

Line 2 generates the package's metadata. (You only have to do this once, and
whenever you modify setup.py.) Line 3 creates the database (db.sqlite) and
inserts initial data. Line 4 serves the website.

Note: If you get an"AssertionError: Unexpected files/directories
in PATH/pyramid_sqla" when trying to install or upgrade pyramid_sqlalchemy,
it's becuase pip gets confused if egg_info files are present in a directory
it's not expecting them. Delete all *\*.egg.info* directories in all
demos, and then try the installation again.

Usage
-----

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

2. In *MyApp/development.ini* change the default database URL to your database:

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
   regardless of what the INI file says, edit *myapp/__init__.py* and uncomment
   the line::

        settings["sqlalchemy.convert_unicode"] = True

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

Managed transactions
--------------------

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

Disabling the transaction manager
+++++++++++++++++++++++++++++++++

If you don't want managed transactions, reconfigure the Session to not have the
extension::

    pyramid_sqla.get_session().config(extension=None)

and also delete the "egg:repoze.tm2#tm" line in the "[pipeline:main]" section
in *development.ini*.  If you disable the manager, you'll have to call
``Session.commit()`` or ``Session.rollback()`` yourself in your views. You'll
also have to configure the application to remove the session at the end of the
request. This would be in an event subscriber but I'm not sure which one.

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

.. autofunction:: add_engine

.. autofunction:: get_session

.. autofunction:: get_engine

.. autofunction:: get_base

.. autofunction:: reset

Logging
-------

The default application template is configured to log SQL queries.
3. The logging is configured to log SQL queries. To change
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
----------------

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



.. _Engine Configuration: http://www.sqlalchemy.org/docs/core/engines.html
.. _Dialects: http://www.sqlalchemy.org/docs/dialects/index.html
.. _Configuring Logging: http://www.sqlalchemy.org/docs/core/engines.html#configuring-logging
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
