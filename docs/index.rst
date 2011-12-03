Akhet
=====
:Version: 2.0b1, released XXXX-XX-XX
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: http://docs.pylonsproject.org/projects/akhet/dev/
:Source: https://bitbucket.org/sluggo/akhet (Mercurial)
:Bugs: https://bitbucket.org/sluggo/akhet/issues
:Discuss: pylons-discuss_ list

Akhet is a set of tutorial-level documentation and convenience code for
Pyramid_. Version 2 focuses more heavily on documentation, and does not contain
an application scaffold [#]_. Instead, the documentation shows how to customize
Pyramid's built-in scaffolds to give a Pylons-like environment. The
documentation gives a walk-through of the default application's structure,
highlighting Useful Bits of Information that are buried in the Pyramid manual
or are not in the manual.  It also discusses some alternative APIs and the
tradeoffs between them. The Akhet library (the convenience classes) are
unchanged in this release.

Akhet 2.0 runs on Python 2.5 - 2.7.   The next version will probably add
Python 3 and drop Python 2.5, as Pyramid 1.3 is doing.



.. toctree::
   :maxdepth: 2

   intro
   vocabulary
   usage
   architecture
   default_content
   transaction_manager
   model_examples
   auth
   testing
   i18n
   migration
   api
   other_pyramid_features
   changes
   unfinished

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".



.. [#] The term "scaffold" is the same as "application template", "paster
   template", and "skeleton". Pyramid has standardized on the term "scaffold"
   to avoid confusion with HTML templates. 


.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/
.. _pylons-discuss: http://groups.google.com/group/pylons-discuss

