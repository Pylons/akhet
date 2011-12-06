Installing Pyramid and Creating Applications
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Here are the basic steps to install Pyramid and Akhet and create an
application. For more details see the `Installing Pyramid`_ and `Creating a
Pyramid Project`_ chapters in the Pyramid manual.  New users should also do
the `SQLAlchemy + URL Dispatch Wiki Tutorial`_, which explains Pyramid while
you build a simple wiki application. 

The steps here are effectively the same as
the installation chapter of the Wiki tutorial; we're just using pip rather than
other installation commands because it makes uninstallation easier, and because
it's the `new hotness`_. We also activate the virtualenv_, which allows us to
keep the application source outside the virtualenv without having to type
convoluted paths to run virtualenv commands. Keeping the application outside
the virtualenv makes it easier to delete/recreate the virtualenv if it gets
hosed, and to run the application under multiple virtualenvs (e.g., to see how
it works under different Python versions, different Pyramid versions, and
different dependency versions). 

Our sample application is called "Zzz"; it contains a Python package ``zzz``. A
prebuilt tarball is available: Zzz.tar.gz_ [#]_.  The following chapters will
walk through this default application.

These steps assume you have Python, virtualenv_, and SQLite_ installed.

Creating an application with Pyramid 1.3 and Akhet
==================================================

(Pyramid 1.3 is unreleased as of this writing. This alternative won't work
until it's released, so use one of the other two alternatives instead.)

.. code-block:: console

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install 'Pyramid>=1.3'
    (myvenv)$ pip install Akhet
    (myvenv)$ pcreate -s alchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ pip install -e .
    (myenv)$ populate_Zzz development.ini
    (myenv)$ pserve development.ini


Creating an application with Pyramid 1.2 and Akhet
==================================================

.. code-block:: console

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ pip install 'Pyramid<1.3'
    (myvenv)$ pip install Akhet
    (myvenv)$ paster create -t routesalchemy Zzz
    (myenv)$ cd Zzz
    (myenv)$ pip install -e .
    (myenv)$ populate_Zzz development.ini
    (myenv)$ paster serve development.ini


Creating an application with development versions of Pyramid and Akhet
======================================================================

Installing Akhet from its source repository works like most Python
repositories. Pyramid, however, requires additional steps.

.. code-block::  console

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
* The extra "./" is so that "pip install -e" recognizes the argument as a path
  name rather than as something to download from PyPI.


Observations
============

The "--no-site-packages" option is recommended for Pyramid; it isolates the
virtualenv from packages installed globally on the computer, which may be
incompatible or have conflicting versions. If you have trouble installing a
package that has C extensions (e.g., a database library, PIL, NumPy), you can
try making a symlink from the virtualenv's site-packages directory to the OS
version of the package; it may take some jiggering to make the package happy.

I found --no-site-packages necessary on Ubuntu 10 because Ubuntu installs
some Zope packages but not all the ones Pyramid needs, and ``zope`` is a
namespace package which can't be split between the global directory and the
virtualenv. I have not had this problem with Ubuntu 11.10 so far, so it may be
fixed.

"pip install -e ." installs the application and all dependencies listed in
setup.py. That's necessary for this application because it depends on
SQLAlchemy, which is not installed with raw Pyramid. Installation also sets up
the 'populate_Zzz' command. In a simpler application without these restrictions
(such as the 'starter' scaffold), you can get by without installation. You'll
have to run "python setup.py egg_info" instead (which updates the
distribution's metadata, and is one of the installation steps. Also, if you
don't install the application, you'll have to always chdir to the application's
directory before running it, because Python won't be able to import it
otherwise.

**Remember for later:** whenever you add or delete a file in the application
directory, run "python setup.py egg_info" to update the metadata.

See `Uninstalling <appendix/uninstalling.html>`_ if you want to uninstall
things later.

Uninstalling
============

To uninstall an application or package that was installed via pip, use "pip
uninstall":

.. code-block:: console

   (myvenv)$ pip uninstall Zzz

If you installed it via "easy_install", "python setup.py install", or "python
setup.py develop", you'll have to uninstall it manually.  Chdir to the
virtualenv's *site-packages* directory. Delete any subdirectories and files
corresponding to the Python package, its metadata, or its egg link. For our
sample application these would be *zzz* (Python package), *Zzz.egg-info* (pip
egg_info), *Zzz.egg* (easy_install directory or ZIP file), and *Zzz.egg-link*
(egg link file). Also edit *easy-install.pth* and delete the application's line
if present.


.. [#] The tarball was built with Pyramid 1.3-dev (2011-12-02, rev.
   d5666e630a08c943a22682540aa51174cee6851f), Python 2.7.2, on Ubuntu 11.10
   (Linux). 


.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _SQLite: http://sqlite.org
.. _submodules: http://schacon.github.com/git/git-submodule.html
.. _Zzz.tar.gz: _static/Zzz.tar.gz
.. _Installing Pyramid: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html
.. _Creating a Pyramid Project: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html
.. _SQLAlchemy + URL Dispatch Wiki Tutorial: http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/installation.html
.. _new hotness: http://python-distribute.org/pip_distribute.png
