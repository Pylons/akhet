Paster Commands
%%%%%%%%%%%%%%%

As in Pylons, the "paster" command creates and runs applications.

paster create
-------------

**paster create** works the same in both Pylons and Pyramid:

.. code-block:: sh

    $ paster create -t akhet Zzz

This is how you create a new application. Our sample application is named
"Zzz". It will ask whether to preconfigure SQLAlchemy in the application; the
default is true. Answer 'n' to skip SQLAlchemy. You can also pass the answer on
the command line:

.. code-block:: sh

    $ paster create -t akhet Zzz sqlalchemy=n

The SQLAlchemy question is specific to the 'akhet' application skeleton. Other
skeletons may have other questions or no questions. (We use the phrase
"skeleton" rather than the traditional "application template" because the
latter is ambiguous and can be confused with a template file.) 

The **application name** must be a valid Python identifier. I.e., it must start
with a letter or underscore; and may contain only letters, numbers, and
underscore. "paster create" will automatically generate the Python **package
name** by lowercasing the application name. 

You can't use an application name that's identical to a module in the Python
standard library.  Paster will create it but Python won't be able to run it. So
don't name your application "Test".

paster serve
------------

**paster serve** also works the same:

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
"zzz" regardless of the actual application name:

.. code-block:: sh

    $ paster proutes development.ini zzz

This replaces "paster routes" in Pylons.

Other paster commands
---------------------

**paster pshell** is covered in the Shell_ section of the Architecture chapter.
It replaces "paster shell" in Pylons.

"paster make-config" is not supported in Pyramid. Instead, all Pyramid
skeletons include a production.ini. You can copy it to make other
INI files.

"paster setup-app" is not supported in Pyramid. Instead, Akhet includes a
*create_db* script. After you have defined your models, run it to create the
database tables. You can customize the script if you want to prepopulate the
dataabse with certain initial records:

.. code-block:: sh

    $ python -m zzz.scripts.create_db development.ini

You can also put other utility scripts in the "scripts" package and run them
the same way.

"paster controller" and "paster restcontroller" do not exist in Pyramid. You'll
have to create your handler modules by hand or copy an existing module.


.. _Shell: architecture.html#shell
