pyramid_sqla
============

**pyramid_sqla** is a library for Pyramid_ applications using SQLAlchemy_, and
an application template that configures the model and other things similar to
Pylons 1 (but not identical).  If follows the philosophy of "make the
simple things simple and the complex things possible".

The current version is 0.1. This is a proof-of-concept release; the API is
subject to change depending on user feedback. The goal is a 1.0 release before
Pyramid 1.0.

.. _SQLAlchemy: http://sqlalchemy.org/
.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/

Current features in the library
-------------------------------

* A SQLAlchemy scoped session, a place to register database engines, and a
  declarative base. These all replace the ``meta`` module in Pylons 1
  applications, making it easier to structure module code freely without
  circular imports
* Initialization requires just one line in __init__.py per database, and no
  boilerplate code in model
* Session management à la TurboGears. This commits all changes at the end of a 
  request, or rolls them back if an exception has occurred. You can still
  commit and roll back on demand, and even prevent other parts of the
  application from committing during the request.

Current features in the application template
--------------------------------------------

* The model, application settings, middleware, and logging are preconfigured
  for a Pylons 1-like SQLAlchemy application
* The static directory is served under "/" instead of "/static", allowing you
  to serve "/robots.txt" as in Pylons 1 but more efficiently
* A sample production.ini is included
* Routing using URL dispatch and view handlers, similar to Routes and
  controllers in Pylons 1
* Listen on localhost:5000 by default (localhost for security, 5000 per Pylons
  1 precedent)
* Templates ending in .html are passed to Mako (or to your desired templater)
* Template globals  ``url`` and ``h`` are configured (for generating URLs and
  a user-defined helper library, respectively). You can change these in the
  subscribers module.
* Configures logging in .ini and handlers
* It has a pony and a unicorn (Paste Pony)

pyramid_sqla has five dependencies: Pyramid_, SQLAlchemy_, repoze.tm2_, and
zope.sqlalchemy_ (for ZopeTransactionExtension, required by repoze.tm2), and
transaction_. It was written on Python 2.6 but should work on 2.5.

.. _zope.sqlalchemy: http://pypi.python.org/pypi/zope.sqlalchemy
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _repoze.tm2: http://docs.repoze.org/tm2/
.. _transaction: http://pypi.python.org/pypi/transaction


Documentation
-------------

.. toctree::
   :maxdepth: 1

   manual
   model_examples
   application_templates
   bugs
   changes

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

