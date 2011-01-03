pyramid_sqla
============

**pyramid_sqla** is library and application template and library for
SQLAlchemy_-powered Pyramid_ applications. The template preconfigures a
Pyramid-SQLAlchemy application, and also includes a few non-database features
borrowed from Pylons 1 for those who like that application struture. The library provides a scoped session
and a central place to register database engines, and an optional declarative
base for your ORM classes.

.. _SQLAlchemy: http://sqlalchemy.org/
.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/

It includes
an application template that preconfigures a Pyramid-SQLAlchemy application
a library and a Paster application template that preconfigures a
Pyramid-SQLAlchemy appliction 
includes a Paster application template. It provides
a scoped session for the application, a central place to register engines, 
a central database session and an engine registry, and manages
commits/rollbacks centrally like TurboGears does, using the repoze.tm2_
transaction middleware.  Unlike the Pylons 1 application template, there's no
"meta" module or "init_model()" function in the application's model. Instead,
the things that were in meta have been moved into the library itself. This
makes it easier to keep your model in a package without interdependencies
between the modules, because each module just imports the library.

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


Documentation
-------------

.. toctree::
   :maxdepth: 1

   manual
   model_examples
   application_templates

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

