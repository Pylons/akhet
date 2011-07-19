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

**Important**: Whenever you add or delete files in the application, remember to
re-execute the "python setup.py egg_info" step before running the application
again. This updates the package's metadata to reflect the new files. Otherwise
Python may not be able to find them.

Installing the application
==========================

So far we haven't installed the application, so Python is looking in the
current directory for the ``zzz`` package and ``Zzz.egg-info`` metadata. This
is convenient during early development because we can create and delete scrath
applications quickly without installing them into the virtualenv and
uninstalling them. However, for production and beta testing you should formally
install the application; that way you can run it from any directory (by
specifying the path to the INI file). 

You can install a link to the application's source directory by running "pip
install -e .". This installs an "egg link" file pointing to the source
directory, so that Python will immediately see any changes in the source. This
is useful in development, and some production deployments also use this system.

The other option is to install a snapshot of the application's current state.
This copies the package's files to the virtualenv's *site-packages* directory,
so that Python will not see any subsequent changes in the source until you
reinstall the application. The command for this is "pip install .". This is the
same thing that happens when you install a third-party package (e.g., "pip
install Akhet").

If you're using easy_install rather than pip, the command to install an egg
link is "python setup.py develop". The command to install a snapshot is
"easy_install ." or "python setup.py install".

Uninstalling the application
============================

To uninstall an application that was installed as a pip snapshot, cd to a
distant directory (not the application source or its parent) and run "pip
uninstall Zzz". This should supposedly work with a pip egg link too but it
hasn't always worked for me. It also works with external packages that were
installed with pip; e.g., "pip uninstall Akhet".

Easy_install does not have an uninstall command, so you'll have to uninstall it
manually in that case.

To uninstall the application (or any Python package) manually, cd to the
virtualenv's *site-packages* directory. Delete any subdirectories and files
corresponding to the Python package, its metadata, or its egg link. For our
sample application these would be *zzz* (Python package), *Zzz.egg-info*
(pip egg_info), *Zzz.egg* (easy_install directory or ZIP file), and
*Zzz.egg-link* (egg link file). Also look in *easy-install.pth* and delete
the application's line if present.


.. _Pyramid documentation: http://docs.pylonsproject.org/
.. _Pyramid tutorials: http://docs.pylonsproject.org/projects/pyramid_tutorials/dev/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Installing Pyramid: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/install.html

