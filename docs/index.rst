Akhet
%%%%%

:Version: 2.0, released 2012-02-12
:Docs-Updated: same
:PyPI: http://pypi.python.org/pypi/Akhet
:Docs: http://docs.pylonsproject.org/projects/akhet/dev/
:Source: https://github.com/Pylons/akhet
:Bugs: https://github.com/Pylons/akhet/issues
:Discuss: pylons-discuss_ list
:Author: `Mike Orr <mailto:sluggoster@gmail.com>`_
:Contributors: Michael Merickel, Marcin Lulek

Akhet is a Pyramid_ library and demo application with a Pylons-like feel.

**Main changes in version 2: (A)** The 'akhet' scaffold gone, replaced by a demo
application, which you can cut and paste from. **(B)** General Pyramid/Pylons
material has been moved out of the manual to the `Pyramid Cookbook`_, section
`Pyramid for Pylons Users`_ guide. *(The guide is not yet online as of February
2012.)* **(C)** The include for static routes has changed to "akhet.static", but
"akhet" is still allowed for backward compatibility. **(D)** A new pony module.
**(E)** The repository is now on GitHub in the Pylons Project.

The demo is distributed separately from the Akhet. Its repository URL is in the
Demo section.

Akhet runs on Python 2.5 - 2.7. Version 2 has been tested on Pyramid
1.3a6 and 1.2.4 using Pyramid 2.7.2 on Ubuntu Linux 11.10.  The next Akhet
version, 2.1, will focus on Python 3 and will drop Python 2.5.
The demo application currently has the same compatibility range as Akhet
itself.

The word "akhet" is the name of the hieroglyph that is Pylons' icon: a sun
shining over two pylons. It means "horizon" or "mountain of light".

Documentation Contents
======================

.. toctree::
   :maxdepth: 2

   library/index
   demo/index

.. toctree::
   :maxdepth: 1

   changes
   rant_scaffold

.. 
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`




.. include:: links.rst
