Akhet
=====
:Version: 2.0, released XXXX-XX-XX
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: http://docs.pylonsproject.org/projects/akhet/dev/
:Source: https://github.com/Pylons/akhet
:Bugs: https://github.com/Pylons/akhet/issues
:Discuss: pylons-discuss_ list

Akhet is a Pyramid_ library and demo application with a Pylons-like feel.
Earlier versions had an application scaffold, but version 2 replaces
it with the demo app. Much of the version 1 manual was moved to the `Pyramid
Cookbook`_ (as the `Pyramid for Pylons Users`_ guide).  
(The guide is not yet available as of January 2012.) 
The Akhet Python library is unchanged in version 2.

The library and demo app have different dependencies and goals, so the demo app
is distribued separately. The library focuses on backward compatibility,
minimal dependencies, and accepts only things that can be maintained long-term.
The demo app is more adventurous, and may contain incompatible changes from
version to version. The demo's main purpose is to contain the templates,
stylesheets, and large chunks of code from the old scaffold that you may want
to copy into your application. In the future, the demo will become more of a
testing ground for new techniques.

The library runs on Python 2.5 - 2.7, and has been tested with Pyramid
1.3a6 and 1.2.4 on Ubuntu Linux 11.10.  The next version will focus on Python 3
support and will drop Python 2.5. The demo app currently has the same
compatibility range as the library.



.. toctree::
   :maxdepth: 2

   library/index
   demo/index

.. toctree::
   :maxdepth: 1

   changes
   unfinished
   rant_scaffold

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".


.. include:: links.rst
