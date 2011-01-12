pyramid_sqla
============
:Version: 0.1 released XXXX-XX-XXX
:Docs:
:Download: 
:PyPI:
:Source: http://bitbucket.org/sluggo/pyramid_sqla (Mercurial)


**pyramid_sqla** is a library for Pyramid_ applications using SQLAlchemy_, and
an application template that configures the model and other things similar but
not identical to Pylons 1.  If follows the philosophy of "make the
simple things simple and the complex things possible".

Version 0.1 is an initial proof-of-concept release; the API is subject to
change depending on user feedback. The goal is a 1.0 release before Pyramid
1.0.

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
* The static directory is served under "/" instead of "/static", overlaying 
  your dynamic URLs
* Routing using URL dispatch and view handlers, similar to Routes and
  controllers in Pylons 1
* Listen on localhost:5000 by default (localhost for security, 5000 per Pylons
  1 precedent)
* Templates ending in .html are passed to Mako (or to your desired templater)
* A helpers module and the ``h`` template global. (You can change template
  globals in the subscribers module.)
* A separate logger is configured for the application package, and is added to
  the handlers module
* Configures logging in .ini and handlers
* A script to initialize your database

pyramid_sqla has five dependencies: Pyramid_, SQLAlchemy_, repoze.tm2_, 
zope.sqlalchemy_, and transaction_. It's tested on Python 2.6/Linux but should
work on 2.5 and other platforms. A set of unit tests is included.

.. _zope.sqlalchemy: http://pypi.python.org/pypi/zope.sqlalchemy
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _repoze.tm2: http://docs.repoze.org/tm2/
.. _transaction: http://pypi.python.org/pypi/transaction


Documentation
-------------

.. toctree::
   :maxdepth: 1

   usage
   non_database_features
   model_examples
   bugs
   changes

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

