pyramid_sqla manual
===================

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

1. Add it to your list of 'requires' dependencies in *setup.py*.

2. In your *development.ini* file add:

   .. code-block:: ini

        sqlalchemy.url = sqlite:///%(here)s/db.sqlite

   You can also add any SQLALchemy engine options such as:

    .. code-block:: ini

        sqlalchemy.pool_recycle = 3600
        sqlalchemy.convert_unicode = true

3. Add the repoze.tm2 middleware to the pipeline:

   .. code-block:: ini

        [pipeline:main]
        pipeline =
            egg:WebError#evalerror
            egg:repoze.tm2#tm
            MyApp

    (Replace "myapp" with your application name, corresponding to the
    "[app:myapp]" section.)

4.  To log SQL queries, modify the "[logger_sqlalchemy]" section in
    *development.ini*. Set ``level = INFO`` to log all queries, ``level =
    DEBUG`` to log queries and results (very verbose!), or ``level = WARN`` to
    log neither. If your *development.ini* does not have a
    "[logger_sqlalchemy]" section, create a new Pyramid application and copy
    all the logging sections from its *development.ini*.

5. In *myapp/__init__.py*, add the following at the top::

        import pyramid_sqla

   Then inside the ``main()`` function, add this like::

        pyramid_sqla.init_dbsession(settings, prefix="sqlalchemy.")

6. In models or views or anywhere else you need them::

        import pyramid_sqla

        Session = pyramid_sqla.get_dbsession()
        engine = pyramid_sqla.get_dbengine()

Note that ``get_dbsession()`` returns a SQLAlchemy `scoped session`_
not a plain SQLAlchemy session.

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

Multiple databases
------------------

API
---

.. currentmodule:: pyramid_sqla

.. automodule:: pyramid_sqla

.. autofunction:: init_dbsession

.. autofunction:: get_dbsession

.. autofunction:: get_dbengine

