Akhet
=====
:Version: 1.0b1, released XXXX-XX-XX
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: https://bitbucket.org/sluggo/akhet/wiki/html/index.html
:Source: https://bitbucket.org/sluggo/akhet (Mercurial)


**Akhet** is a Pylons-like application template for the Pyramid_ web framework,
along with a small support library to make Pyramid a bit easier to use. The
documentation can serve as an introduction to the Pyramid manual for all new
Pyramid users, and it shows the differences between Pyrmaid and Pylons.

Version 1.0b1 is a public beta to give it some testing before the final
release. Please send feedback to the pylons-discuss_ list. The Akhet package was
previously named "pyramid_sqla"; it was changed to reflect its evolution from a
SQLALchemy application template to a more full-fledged Pylons-like template.
The SQLAlchemy library was spun off to the "SQLAHelper" package.

The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".

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


Documentation
-------------

.. toctree::
   :maxdepth: 1

   usage
   vocabulary
   migration
   unfinished-usage
   non_database_features
   model_examples
   bugs
   changes

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

