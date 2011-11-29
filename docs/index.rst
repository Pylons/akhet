Akhet
=====
:Version: 2.0, released XXXX-XX-XX
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: http://docs.pylonsproject.org/projects/akhet/dev/
:Source: https://bitbucket.org/sluggo/akhet (Mercurial)
:Bugs: https://bitbucket.org/sluggo/akhet/issues
:Discuss: pylons-discuss_ list

Akhet is a set of tutorial-level documentation and convenience code for
Pyramid_. Version 2 focuses more heavily on documentation, and does not contain
an application scaffold [#]_. Instead of a scaffold, the
documentation shows how to customize Pyramid's built-in scaffolds to give a
Pylons-like environment. The Akhet library (the ``akhet`` Python package) is
still around; it's unchanged in this release.

Akhet 2.0 runs on Python 2.5 - 2.7.   The next version will probably add
Python 3 support and drop Python 2.5, as Pyramid 1.3 is doing.



.. toctree::
   :maxdepth: 1

   intro
   vocabulary
   usage
   paster
   architecture
   default_content
   transaction_manager
   model_examples
   auth
   testing
   i18n
   migration
   upgrading
   api
   other_pyramid_features
   changes

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".



.. [#] The term "scaffold" has replaced "application template" and "paster
   template" to avoid confusion with HTML templates. 


.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/
.. _pylons-discuss: http://groups.google.com/group/pylons-discuss

