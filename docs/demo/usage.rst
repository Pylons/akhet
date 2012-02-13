Usage and features
%%%%%%%%%%%%%%%%%%

The Akhet demo application shows the Akhet library's features in action, and
contains templates and code you can copy into your own application as a
starting point. The demo is based on the former Akhet application scaffold
from Akhet 1, and what users of that scaffold have later reported doing in
their more recent applications.

The demo is distributed separately from Akhet due to its larger number of
dependencies and more frequent changes.  The Akhet library focuses on stability
and backward compatibility, while the demo is free to experiment more and make
backward-incompatible changes, and is in a permanent development mode.

Installation
============

You can install the demo it from its source repository like any Pyramid
application:

.. code-block::  console

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ git clone git://github.com/mikeorr/akhet_demo
    (myenv)$ pip install -e .
    (myenv)$ pserve development.ini

Features
========

The demo has the following features which originated in the former 'akhet'
scaffold:

* Mako templates.
* Site template to provide a common look and feel to your pages.
* Automatically recognize filenames ending in .html as Mako templates.
* Default stylesheet and browser-neutral reset stylesheet.
* Pylons-like template globals including a helpers module 'h' and a URL
  generator 'url', and instructions for adding additional ones.
* Serve static files at any URL, without being limited by URL prefixes.
* Listen on localhost:5000 by defalt.
* Beaker session and cache configuration.
* Demonstration of flash messages and logging.


The demo introduces the following new features:

* Class-based views using ``@view_config``.
* A pony and a unicorn.

The demo does *not* have these features that were in the former 'akhet'
scaffold:

* A SQLAlchemy model. The Pyramid 'alchemy' scaffold and the Models chapter in
  the `Pyramid for Pylons Users`_ guide are sufficient to get started.
* View handlers using 'pyramid_handlers'. Many Akhet users have gone to
  class-based views using Pyramid's standard ``@view_config``, so the demo is
  doing that now too.
* Subpackages for views and models. These are easy enough to create yourself if
  you need them.



.. include:: ../links.rst
