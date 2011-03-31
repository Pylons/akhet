Paster Commands
%%%%%%%%%%%%%%%

As in Pylons, the "paster" command creates and runs applications.

paster create
-------------

**paster create** works the same in both Pylons and Pyramid:

.. code-block:: sh

    $ paster create -t akhet Zzz

This is how you create a new application, as described earlier in the Usage
chapter. Our sample application is named "Zzz". It will ask certain questions.
Currently it asks whether to preconfigure SQLAlchemy in the application; the
default is true. Answer 'n' to skip SQLAlchemy. You can also pass the answer on
the command line:

.. code-block:: sh

    $ paster create -t akhet Zzz sqlalchemy=n

The SQLAlchemy question is specific to the 'akhet' application skeleton. Other
skeletons may have other questions or no questions. (Paster calls the
application skeleton a "template" but we avoid that term because it can be
confused with a template file.)


paster serve
------------

**paster serve** also works the same as in Pylons:

.. code-block:: sh

    $ paster serve development.ini
    $ paster serve --reload development.ini

This runs the application under PasteHTTPServer or another server specified in
the INI file. Running it under Apache or another Python webserver works the
same way as in Pylons; see the Pyramid manual for details.

paster proutes
--------------

**paster proutes** prints the current route definitions. You have to specify
both the INI file and the application section in the file, which for Akhet is
"myapp" regardless of the actual application name:

.. code-block:: sh

    $ paster proutes development.ini myapp

This replaces "paster routes" in Pylons.

Other paster commands
---------------------

**paster pshell** is covered in the Shell_ section of the Architecture chapter.
It replaces "paster shell" in Pylons.

"paster make-config" is not supported in Pyramid. Instead, all Pyramid
skeletons include a *production.ini*. You can copy it to make other
INI files.

"paster setup-app" is not supported in Pyramid. Instead, Akhet includes a
*create_db.py* script. After you have defined your models, run it to create the
database tables:

.. code-block:: sh

    $ python -m zzz.scripts.create_db development.ini

You can customize the script if you want to prepopulate the
databse with certain initial records.
You can also put other utility scripts in the "scripts" package and run them
the same way.

"paster controller" and "paster restcontroller" do not exist in Pyramid. You'll
have to create your handler modules by hand or copy an existing module.


.. _Shell: architecture.html#shell
