Usage
%%%%%

Installing Akhet
================

Install Akhet like any Python package, using either "pip install Akhet" or
"easy_install Akhet". To check out the development repository use "hg clone
https://bitbucket.org/sluggo/akhet". Pyramid is a dependency of Akhet so it
will be automatically installed.

It's generally a good idea to install Akhet into a virtualenv_. If you're
unfamiliar with installing Python, Virtualenv, and Setuptools/Distribute, see
the `Installing Pyramid`_ chapter in the Pyramid manual. I use the OS packages
in Ubuntu Linux 10.10: python-setuptools, python-virtualenv, and
virtualenvwrapper.

.. code-block:: sh

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install Akhet
    ...

You'll probably need Virtualenv's ``--no-site-packages`` option as above to
avoid undesired interactions with with other Python packages installed globally
(outside the virtualenv). I had particular trouble due to some Zope packages
Ubuntu installs by default. If you need certain global packages (e.g., those
with C dependencies that can be hard to install yourself), make symbolic links
to them in the virtualenv's site-packages.


Creating an application
=======================

Create an application with Paster using the "akhet" application skeleton.

.. code-block:: sh

    (myvenv)$ paster create -t akhet Zzz
        Selected and implied templates:
      Akhet#akhet  A Pylons-like Pyramid project

    Variables:
      egg:      Zzz
      package:  zzz
      project:  Zzz
    Enter sqlalchemy (Include SQLAlchemy configuration? (y/n)) [True]:
    ...
    Copying setup.py_tmpl to ./Zzz/setup.py
    Running /home/sluggo/.virtualenvs/pyramid/bin/python setup.py egg_info
    (myvenv)$ 

You can answer the question on the command line so that it won't prompt you:

.. code-block:: sh

    (myvenv)$ paster create -t akhet Zzz sqlalchemy=y

Our sample application is called "Zzz". It has a top-level directory "Zzz"
containing a Python package ``zzz`` (lowercase). Throughout this manual we'll
use Zzz and zzz as shorthands for your application name and package name. You
can name your application anything, but don't use "Test" or any other name in
the Python standard library, otherwise it won't run. It's easiest to stick with
a valid Python identifier: a letter or underscore followed by zero or more
letters, numbers, or underscores.

Install the application's dependencies. For convenience these are listed both
in a *requirements.txt* file and in *setup.py*.

.. code-block:: sh

    (myvenv)$ cd Zzz
    (myvenv)$ pip install -r requirements.txt
    ...

Generate the package's metadata ("egg_info" files):

.. code-block:: sh

    (myvenv)$ python setup.py egg_info
    running egg_info
    writing requirements to Zzz.egg-info/requires.txt
    writing Zzz.egg-info/PKG-INFO
    writing top-level names to Zzz.egg-info/top_level.txt
    writing dependency_links to Zzz.egg-info/dependency_links.txt
    writing entry points to Zzz.egg-info/entry_points.txt
    writing paster_plugins to Zzz.egg-info/paster_plugins.txt
    reading manifest file 'Zzz.egg-info/SOURCES.txt'
    writing manifest file 'Zzz.egg-info/SOURCES.txt'

.. tip::

    Whenever you run the application, re-run this command first *if* you've
    added/deleted any files or modified *setup.py*. You do not have to re-run
    it if you've merely modified the files.

The application should now run out of the box:

.. code-block:: sh

    (venv)$ paster serve development.ini

Go to the URL indicated in your web browser (http://127.0.0.1:5000).
The default application doesn't define any tables or models so it doesn't
actually do anything except display some help links. When you get bored, press
ctrl-C to quit the HTTP.

Building the application
========================

You can now customize the application as you see fit.

If you've never built a (Pylons) web application before, there will be
Akhet-specifc tutorials coming but they're not finished yet. In the meantime,
skim over the Akhet documentation and then go to the Pyramid tutorials. Choose
the ones that say "URL dispatch" and "view handlers" in their introduction;
these are the most similar to Akhet. 

If you're porting an existing Pylons application to Pyramid, the Architecture
and Migration chapters should get you started.

.. _Pyramid documentation: http://docs.pylonsproject.org/
.. _Pyramid tutorials: http://docs.pylonsproject.org/projects/pyramid_tutorials/dev/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Installing Pyramid: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/install.html

