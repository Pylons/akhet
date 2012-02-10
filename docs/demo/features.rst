Usage and Features
%%%%%%%%%%%%%%%%%%

The Akhet demo application includes Mako templates, a stylesheet and reset
stylesheet, and a basic view class to get you started. It shows the Akhet
library features in action. It's based on the former Akhet application scaffold
and what users have reported doing since the scaffold was released.

The demo is not shipped with the Akhet package due to its larger number of
dependencies and more frequent changes.  You can install it from its source
repository like any Pyramid application:

.. code-block::  console

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ git clone git://github.com/mikeorr/akhet_demo
    (myenv)$ pip install -e .
    (myenv)$ pserve development.ini

Features
========

The demo has the following features ported from the former 'akhet' scaffold
(which are not in the standard Pyramid scaffolds):

* Mako templates.
* Site template to provide a common look and feel to your pages.
* Automatically recognize filenames ending in .html as Mako templates.
* Starter stylesheet and browser-neutral reset stylesheet.
* Pylons-like template globals including a helpers module 'h' and a URL
  generator 'url', and instructions for adding additional ones.
* Serve static files at any URL, without being limited by URL prefixes.
* Listen on localhost:5000 by defalt.
* Session configuration.
* Demonstration of flash messages and logging.


The demo introduces the following new features:

* Class-based views using ``@view_config``.
* A pony and a unicorn. (Ported from 'paste.pony'.)

The demo does *not* have the following features from the former 'akhet'
scaffold:

* A SQLAlchemy model. The Pyramid 'alchemy' scaffold and the Models chapter in
  the `Pyramid for Pylons Users`_ guide are sufficient to get started.
* View handlers using 'pyramid_handlers'. Many Akhet users have gone to
  class-based views using Pyramid's standard ``@view_config``, so the demo is
  doing that now too.
* Subpackages for views and models. These are easy enough to create yourself if
  you need them.


.. include:: ../links.rst
