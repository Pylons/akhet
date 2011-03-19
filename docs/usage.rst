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

You'll probably want Virtualenv's ``--no-site-packages`` option to avoid
undesired interactions with with other Python packages installed globally
(outside the virtualenv). In particular, "zope" is a namespace package that
can't be split between the global site-packages and the virtualenv. Ubuntu
installs some Zope packages and that can lead to ImportError unless you use
``--no-site-packages``. If you do need particular global packages (such as those
with C dependencies that can be hard to install yourself), make symbolic links
from the virtualenv's site-packages to the packages in the global
site-packages.

.. code-block:: sh

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install Akhet
    ...

Creating an application
=======================

Create an application with Paster using the "akhet" application skeleton.

.. code-block:: sh

    (myvenv)$ paster create -t akhet MyApp
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


It should work out of the box:

.. code-block:: sh

    (venv)$ cd MyApp
    (venv)$ pip install -e .
    (venv)$ paster serve development.ini

Go to the URL indicated in your web browser (http://127.0.0.1:5000).
The default application doesn't define any tables or models so it doesn't
actually do anything except display some help links. When you get bored, press
ctrl-C to quit the HTTP.

The second line -- "pip install -e ." -- installs the application into the
virtualenv, which also installs its dependencies and updates the package's
metadata (the egg-info directory). The "-e" option installs a link to the
development directory rather than a copy of the application. This may not work
on some systems (Python will complain it can't import the application); in that
case omit the "-e" option.

Building an application
=======================

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

