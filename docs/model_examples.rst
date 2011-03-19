Model Examples
%%%%%%%%%%%%%%

This chapter gives some examples for writing your application models. These are
based on the `SQLAlchemy documentation`_, which should be your primary guide.

These models assume SQLAlchemy 0.6.x and Python >= 2.6. For earlier versions of
Python, use the ``%`` operator instead of the the string ``.format`` method.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/

A simple one-table model
========================

::

    import sqlahelper
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    Base = sqlahelper.get_base()
    Session = sqlahelper.get_session()

    class User(Base):
        __tablename__ = "users"

        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.Unicode(100), nullable=False)
        email = sa.Column(sa.Unicode(100), nullable=False)

This model has one ORM class, ``User`` corresponding to a database table
``users``. The table has three columns: ``id``, ``name``, and ``user``.


A three-table model
===================

We can expand the above into a three-table model suitable for a medium-sized
application.  ::

    import sqlahelper
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    Base = sqlahelper.get_base()
    Session = sqlahelper.get_session()

    class User(Base):
        __tablename__ = "users"

        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.Unicode(100), nullable=False)
        email = sa.Column(sa.Unicode(100), nullable=False)

        addresses = orm.relationship("Address", order_by="Address.id")
        activities = orm.relationship("Activity",
            secondary="assoc_users_activities")

        @classmethod
        def by_name(class_):
            """Return a query of users sorted by name."""
            User = class_
            q = Session.query(User)
            q = q.order_by(User.name)
            return q
        

    class Address(Base):
        __tablename__ = "addresses"

        id = sa.Column(sa.Integer, primary_key=True)
        user_id = foreign_key_column(None, sa.Integer, "users.id")
        street = sa.Column(sa.Unicode(40), nullable=False)
        city = sa.Column(sa.Unicode(40), nullable=False)
        state = sa.Column(sa.Unicode(2), nullable=False)
        zip = sa.Column(sa.Unicode(10), nullable=False)
        country = sa.Column(sa.Unicode(40), nullable=False)
        foreign_extra = sa.Column(sa.Unicode(100, nullable=False))

        def __str__(self):
            """Return the address as a string formatted for a mailing label."""
            state_zip = u"{0} {1}".format(self.state, self.zip).strip()
            cityline = filterjoin(u", ", self.city, state_zip)
            lines = [self.street, cityline, self.foreign_extra, self.country]
            return filterjoin(u"|n", *lines) + u"\n"


    class Activity(Base):
        __tablename__ = "activities"

        id = sa.Column(sa.Integer, primary_key=True)
        activity = sa.Column(sa.Unicode(100), nullable=False)


    assoc_users_activities = sa.Table("assoc_users_activities", Base.metadata,
        foreign_key_column("user_id", sa.Integer, "users.id"),
        foreign_key_column("activities_id", sa.Unicode(100), "activities.id"))
            
    # Utility functions
    def filterjoin(sep, *items):
        """Join the items into a string, dropping any that are empty.
        """
        items = filter(None, items)
        return sep.join(items)

    def foreign_key_column(name, type_, target, nullable=False):
        """Construct a foreign key column for a table.

        ``name`` is the column name. Pass ``None`` to omit this arg in the 
        ``Column`` call; i.e., in Declarative classes.

        ``type_`` is the column type.

        ``target`` is the other column this column references.

        ``nullable``: pass True to allow null values. The default is False
        (the opposite of SQLAlchemy's default, but useful for foreign keys).
        """
        fk = sa.ForeignKey(target)
        if name:
            return sa.Column(name, type_, fk, nullable=nullable)
        else:
            return sa.Column(type_, fk, nullable=nullable)

This model has a ``User`` class corresponding to a ``users`` table, an
``Address`` class with an ``addresses`` table, and an ``Activity`` class with
``activities`` table.  ``users`` is in a 1:Many relationship with
``addresses``.  ``users`` is also in a Many:Many`` relationship with
``activities`` using the association table ``assoc_users_activities``.  This is
the SQLAlchemy "declarative" syntax, which defines the tables in terms of ORM
classes subclassed from a declarative ``Base`` class. Association tables do not
have an ORM class in SQLAlchemy, so we define it using the ``Table``
constructor as if we weren't using declarative, but it's still tied to the
Base's "metadata".

We can add instance methods to the ORM classes and they will be valid for one
database record, as with the ``Address.__str__`` method. We can also define
class methods that operate on several records or return a query object, as with
the ``User.by_name`` method. 

There's a bit of disagreement on whether ``User.by_name`` works better as a
class method or static method. Normally with class methods, the first argument
is called ``class_`` or ``cls`` or ``klass`` and you use it that way throughout
the method, but in ORM queries it's more normal to refer to the ORM class by
its proper name. But if you do that you're not using the ``class_`` variable
so why not make it a static method? But the method does belong to the class in
a way that an ordinary static method does not. I go back and forth on this, and
sometimes assign ``User = class_`` at the beginning of the method. But none of
these ways feels completely satisfactory, so I'm not sure which is best.

Common base class
=================

You can define a superclass for all your ORM classes, with common class methods
that all of them can use. You can't use SQLAHelper's declarative base in this
case because it's already defined with another superclass, so you'll have to
define your own declarative base::

    class ORMClass(object):
        @classmethod
        def query(class_):
            return Session.query(class_)

        @classmethod
        def get(class_, id):
            return Session.query(class_).get(id)

    Base = declarative.declarative_base(cls=ORMClass)
    
    class User(Base):
        __tablename__ = "users"

        # Column definitions omitted

Then you can do things like this in your views::

    user_1 = models.User.get(1)
    q = models.User.query()

Whether this is a good thing or not depends on your perspective.

Multiple databases
==================

The default configuration in the main function configures one database. To
connect to multiple databases, list them all in
*development.ini* under distinct prefixes. You can put additional engine
arguments under the same prefixes. For instance:

.. code-block: ini

    sqlalchemy.url = postgresql://me:PASSWORD@localhost/mydb
    sqlalchemy.logging_name = maindb
    stats.url = sqlite:///%(here)s/scratch.sqlite
    stats.logging_name = sessionsdb

Then modify the main function to add each engine. You can also pass even more
engine arguments that override any same-name ones in the INI file. ::

    engine = sa.engine_from_config(settings, prefix="sqlalchemy.",
        pool_recycle=3600, convert_unicode=True)
    stats = sa.engine_from_config(settings, prefix="stats.")
    sqlahelper.add_engine(engine)
    sqlahelper.add_engine(stats, "stats")

In this scenario, the 'engine' engine was added without a name (no second
argument), so it becomes the default engine named "default". The contextual
session is bound to it, and the declarative base's metadata is bound to it too.
To retrieve it later, call ``sqlahelper.get_engine()``.

The 'stats' engine was added under the name "stats", so it is not bound to
anything. To use it, you must pass the 'bind=stats' argument to any ORM method
or SQL method that executes a query or command, or execute the code directly on
the engine itself::

    # ORM example
    records = Session.query(MyTable).all(bind=stats)

    # SQL example
    sql = sa.select([MyTable.__table__])
    rslt = stats.execute(sql)
    records = rslt.fetchall()

If you're in a function and need a reference to the engine, retrieve it by
name: ``sqlahelper.get_engine("stats")``.

You can, of course, create an engine directly without going through the
application settings::

    engine = sa.create_engine("mysql://me:PASSWORD@localhost/farm")
    sqlahelper.add_engine(engine, "farm")

Two engines, but no default engine
==================================

In this scenario, two engines are equally important, and neither is predominent
enough to deserve being the default engine. This is useful in applications
whose main job is to copy data from one database to another. The configuration
is the same except that we name both engines::

    sqlahelper.add_engine(db1, "db1")
    sqlahelper.add_engine(db2, "db2")

Because there is no default engine, you will have to use the 'bind' argument
for all queries, or execute them directly on the engine.

Different tables bound to different engines
===========================================

You can bind different ORM classes to different engines in the same
database session.  Configure your application with no default engine, and then
call the Session's ``.configure`` method with the ``binds=`` argument to
specify which classes go to which engines. For instance::

    sqlahelper.add_engine(db1, "db1")
    sqlahelper.add_engine(db2, "db2")
    Session = sqlahelper.get_session()
    import zzz.models as models
    binds = {models.Person: db1, models.Score: db1}
    Session.configure(binds=binds)

The keys in the ``binds`` dict can be SQLAlchemy ORM classes, table objects, or
mapper objects.


Reflected tables
================

Reflected tables pose a dilemma because they depend on a live database
connection in order to be initialized. But the engine may not be configured yet
when the model is imported. SQLAHelper does not address this issue
directly. Pylons 1 models traditionally have a ``model.init_model(engine)``
function which performs any initialization that requires a live connection.
Pyramid applications typically do not need this function because the Session,
engines, and base are initialized in the ``sqlahelper`` library before the
model is imported. But in the case of reflection, you'll probably need an 
``init_model`` function that sets global variables. You'll just have to
remember to call the function before using anything in the model.

If you're using SQLAlchemy's declarative syntax as in the examples above, we
*think* you'd have to define the entire ORM class inside the function, and use
a ``global`` statement to put the class into the module namespace.

If you're not using declarative, the ORM class can be defined at module level,
but the table will have to be defined in the function with a ``global``
statement, and the mapper call will also have to be in the function.


.. _Engine Configuration: http://www.sqlalchemy.org/docs/core/engines.html
.. _Dialects: http://www.sqlalchemy.org/docs/dialects/index.html
.. _Configuring Logging: http://www.sqlalchemy.org/docs/core/engines.html#configuring-logging
.. _scoped session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _Using a Commit Veto: http://docs.repoze.org/tm2/#using-a-commit-veto

