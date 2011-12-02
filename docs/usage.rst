Usage
%%%%%

Creating a Pyramid/Akhet application
====================================

Here are the basic steps to install Pyramid and Akhet, create a virtualenv and
activate it, create an application, and run it so you can see it in the
browser. The sample application is called "Zzz"; it contains a Python package
``zzz``.

For Pyramid 1.3 (unreleased; this won't work until it's released):

.. code-block:: sh

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install 'Pyramid>=1.3'
    (myvenv)$ pip install Akhet
    (myvenv)$ pcreate -s alchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ pip install -e .
    (myenv)$ populate_Zzz development.ini
    (myenv)$ pserve development.ini

For Pyramid 1.2 and earlier:

.. code-block:: sh

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install 'Pyramid<1.3'
    (myvenv)$ pip install Akhet
    (myvenv)$ paster create -t routesalchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ pip install -e .
    (myenv)$ populate_Zzz development.ini
    (myenv)$ paster serve development.ini

Throughout this manual we'll use "Zzz" for your application's name, and ``zzz``
for the top-level Python module in the application.

The "--no-site-packages" option is recommended for Pyramid; it isolates the
virtualenv from packages installed globally on the computer, which may be
incompatible or have conflicting versions. If you have trouble installing a
package that has C extensions (e.g., a database library, PIL, NumPy), you can
try making a symlink from the virtualenv's site-packages directory to the OS
version of the package; it may take some jiggering to make the package happy.

(I found --no-site-packages necessary on Ubuntu 10, because Ubuntu installs
some Zope packages but not all the ones Pyramid needs, and ``zope`` is a
namespace package which can't be split between the global directory and the
virtualenv.) 

"pip install -e ." installs the application and all dependencies listed in
setup.py. This is necessary with the 'akhet' scaffold to install SQLAlchemy.
In a simpler application with no dependencies, you can get by with just running
"python setup.py egg_info" (which updates the distribution metadata without
installing the distribution) *if* you always chdir to the application's
directory before running it.

Remember for later: whenever you add or delete a file in the application
directory, run "python setup.py egg_info" to update the metadata.

See `Uninstalling <appendix/uninstalling.html>`_ if you want to uninstall
things later.

Using development versions
==========================

Installing Akhet from its source repository works like most Python
repositories. Pyramid, however, requires additional steps.

.. code-block::  sh

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ git clone git://github.com/Pylons/pyramid Pyramid
    (myvenv)$ pip install setuptools-git
    (myvenv)$ pip install -e ./Pyramid
    (myvenv)$ hg clone http://bitbucket.org/sluggo/akhet Akhet
    (myvenv)$ pip install -e ./Akhet
    (myvenv)$ pcreate -s alchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ pip install -e .
    (myenv)$ populate_Zzz development.ini
    (myenv)$ pserve development.ini


Three things to note here:

* Install Pyramid first so that it will satisfy Akhet's Pyramid dependency.
  Otherwise when you install Akhet, it will download the latest stable version
  of Pyramid from PyPI.
* Pyramid requires 'setuptools-git' because the repsository contains Git
  submodules_.
* Pyramid *must* be installed as a link (with "-e") because a regular install
  won't copy the scaffolds or other supplemental files. (That's because the
  repository does not contain a MANIFEST.in file.)

Uninstalling
============

To uninstall an application or package that was installed with pip, use "pip
uninstall":

.. code-block:: sh

   (myvenv)$ pip uninstall Zzz

If you installed it via "easy_install", "python setup.py install", or "python
setup.py develop", you'll have to uninstall it manually.  Chdir to the
virtualenv's *site-packages* directory. Delete any subdirectories and files
corresponding to the Python package, its metadata, or its egg link. For our
sample application these would be *zzz* (Python package), *Zzz.egg-info* (pip
egg_info), *Zzz.egg* (easy_install directory or ZIP file), and *Zzz.egg-link*
(egg link file). Also edit *easy-install.pth* and delete the application's line
if present.


.. _Pyramid documentation: http://docs.pylonsproject.org/en/latest/docs/pyramid.html
.. _Pyramid tutorials: http://docs.pylonsproject.org/projects/pyramid_tutorials/dev/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Installing Pyramid: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/install.html
.. _submodules: http://schacon.github.com/git/git-submodule.html
