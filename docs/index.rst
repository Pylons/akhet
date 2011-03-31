Akhet
=====
:Version: 1.0, released 2011-XX-XX
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: http://docs.pylonsproject.org/projects/akhet/dev/
:Source: https://bitbucket.org/sluggo/akhet (Mercurial)
:Bugs: https://bitbucket.org/sluggo/akhet/issues
:Discuss: pylons-discuss_ list


**Akhet** is a Pylons-like application template (or "skeleton") for the
Pyramid_ web framework, along with a small support library to make Pyramid a
bit easier to use. This manual explains Akhet and also attempts to be a gentle
introduction to the Pyramid manual, which some people find overwhelming at
first. This manual assumes you're familiar with Python web development.

Coming soon: tutorials for new web developers, and a higher-level skeleton with
more batteries. These are being written by third parties.

.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/
.. _pylons-discuss: http://groups.google.com/group/pylons-discuss

Features
--------

* URL dispatch and view handlers, similar to Pylons' Routes and controllers.
* Asks whether to configure SQLAlchemy.
* Sets up a transaction manager for request-wide commit and rollback.
* A script to initialize the database (replaces "paster setup-app").
* Serves static files under "/", mixed with your dynamic URLs.
* Listens on localhost:5000 by default.
* Logging configured in development.ini and production.ini.
* Templates ending in .html are passed to Mako (or to your desired templater)
* A helpers.py module tied to the ``h`` template global.
  (You can also choose your own template globals.)
* "handlers", "models", and "lib" are packages to give plenty of room for large
  applications.
* An extensible home page template, site template, and default stylesheet.


Documentation
-------------

.. toctree::
   :maxdepth: 1

   usage
   vocabulary
   paster
   architecture
   transaction_manager
   model_examples
   auth
   testing
   i18n
   migration
   api
   other_pyramid_features
   bugs
   changes

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Akhet was previously called "pyramid_sqla"; it was changed
to reflect its evolution from a SQLALchemy application skeleton to a more
full-fledged Pylons-like skeleton.  The SQLAlchemy library from pyramid_sqla
was spun off to the "SQLAHelper" package.

The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".

Akhet was developed on Python 2.6 and Ubuntu Linux 10.10. Pyramid runs on
Python 2.4 - 2.7; Mac, Windows, Unix; CPython, Jython, and Google App Engine.
It does not run on Python 3 yet; several dependencies are being updated for
that.
