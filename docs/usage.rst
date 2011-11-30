Usage
%%%%%

Creating a Pyramid/Akhet application
====================================

Here are the basic steps to install Pyramid and Akhet, create a virtualenv and
activate it, create an application, and run it so you can see it in the
browser.

.. code-block:: sh
   :linenos:

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install Pyramid
    (myvenv)$ pip install Akhet
    (myvenv)$ pcreate -s alchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ python setup.py egg_info
    (myenv)$ pserve development.ini

* Line 1 creates the virtualenv. "--no-site-packages" is recommended with
  Pyramid. `Why <appendix/no_site_packages.html>`_
* Line 5 creates application "Zzz" based on the 'alchemy' scaffold.
  (For Pyramid 1.2 and earlier, use "paster create -t routesalchemy Zzz"
  instead.)
* Line 7 generates the package metadata (the *Zzz.egg-info*
  directory). Remember to do this whenever you add or delete files in the
  package.
* Line 8 launches the server using the configuration file
  "development.ini". (For Pyramid 1.2 and earlier, use "paster serve
  development.ini" instead.)

See the `Installing Pyramid`_ chapter in the Pyramid manual if any of this is
unfamiliar. 

.. 
    Go to the URL indicated in your web browser (http://127.0.0.1:5000).  The
    default application doesn't define any tables or models so it doesn't
    actually do anything except display some help links. When you get bored,
    press ctrl-C to quit the HTTP.

Throughout this manual we'll use "Zzz" for your application's name, and ``zzz``
for the top-level Python module in the application.

See `Uninstalling <appendix/uninstalling.html>`_ if you want to uninstall
things later.

Using development versions
==========================

Akhet's development version works like most Python source repositories.
Pyramid's development version requires additional work to install.

.. code-block::  sh

    (myvenv)$ git clone git://github.com/Pylons/pyramid Pyramid
    (myvenv)$ pip install setuptools-git
    (myvenv)$ pip install -e ./Pyramid
    (myvenv)$ hg clone http://bitbucket.org/sluggo/akhet Akhet
    (myvenv)$ pip install -e ./Akhet

Three things to note here:

* Pyramid requires 'setuptools-git' because the repsository contains Git
  submodules_.
* Pyramid *must* be installed as a link (with "-e") because the repository does
  not contain a MANIFEST.in file, so a regular install wouldn't copy the
  scaffolds or other supplemental files.
* Install Pyramid *before* Akhet in order to satisfy the dependency. Otherwise
  installing Akhet would download the latest stable Pyramid from PyPI.


The "p" commands
================

Pyramid 1.3 includes the following command-line utilities:

* **pcreate**: Create a new application using a scaffold.
* **pserve**: Launch an application and server based on an INI configuration
  file.
* **proutes**: List all routes in an application.
* **pviews**: List all views in an application.
* **pshell**: An interactive Python shell preloaded with your application
  environment.
* **ptweens**: List all tweens.


.. _Pyramid documentation: http://docs.pylonsproject.org/
.. _Pyramid tutorials: http://docs.pylonsproject.org/projects/pyramid_tutorials/dev/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Installing Pyramid: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/install.html
.. _submodules: http://schacon.github.com/git/git-submodule.html
