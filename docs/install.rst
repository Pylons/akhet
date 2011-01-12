Installation and Demos
%%%%%%%%%%%%%%%%%%%%%%

Install pyramid_sqla like any Python package, using either "pip install
pyramid_sqla" or "easy_install pyramid_sqla". To check out the development
repository: "hg clone http://bitbucket.org/sluggo/pyramid_sqla". 

There's one demo application in the source distribution but it doesn't do much
yet. It displays your database URL. The create_db script puts a sample record
in a table. It has a pony and a unicorn (using Paste Pony). To run it, first
install pyramid_sqla, then do:

.. code-block:: sh
   :linenos:

    $ cd demos/SimpleDemo
    $ python setup.py egg_info
    $ python -m simpledemo.scripts.create_db development.ini
    $ paster serve development.ini

Line 2 generates the package's metadata. (You only have to do this once, and
whenever you modify setup.py.) Line 3 creates the database (db.sqlite) and
inserts initial data. Line 4 serves the website.

Note: If you get an"AssertionError: Unexpected files/directories
in PATH/pyramid_sqla" when trying to install or upgrade pyramid_sqlalchemy,
it's becuase pip gets confused if egg_info files are present in a directory
it's not expecting them. Delete all *\*.egg.info* directories in all
demos, and then try the installation again.

