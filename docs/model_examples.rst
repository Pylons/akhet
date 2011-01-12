Model Examples
==============

This chapter gives some examples for writing your application models. These are
based on the `SQLAlchemy documentation`_, which should be your primary guide.

These models assume SQLAlchemy 0.6.x and Python >= 2.6. For earlier versions of
Python, use the ``%`` operator instead of the the string ``.format`` method.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/

A simple one-table model
------------------------

::

    import pyramid_sqla as psa
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    Base = psa.get_base()
    Session = psa.get_session()

    class User(Base):
        __tablename__ = "users"

        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.Unicode(100), nullable=False)
        email = sa.Column(sa.Unicode(100), nullable=False)

This model has one ORM class, ``User`` corresponding to a database table
``users``. The table has three columns: ``id``, ``name``, and ``user``.


A three-table model
-------------------

We can expand the above into a three-table model suitable for a medium-sized
application. (This example uses the string ``.format`` method introduced in
Python 2.6. In older versions, use the ``%`` operator instead.) ::

    import pyramid_sqla as psa
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    Base = psa.get_base()
    Session = psa.get_session()

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

There are arguments both ways on whether ``User.by_name`` should be a class
method or a static method. Normally in a class method you'd use the ``class_``
variable so that it would refer to the subclass in subclasses, but using the
class's proper name (``User``) makes queries easier to read, and ORM classes
are rarely subclassed anyway. Here we split the difference by using a class
method but creating a local variable with the same name as the class to use in
queries. It's hard to say whether this is the best way or not, so take your
pick.

Common base class
-----------------

You can define a superclass for all your ORM classes, with common class methods
that all of them can use. You can't use ``pyramid_sqla.Base`` in this case
though so you'll have to define your own declarative base::

    class ORMClass(object):
        @classmethod
        def query(class_):
            return pyramid_sqla.get_dbsession().query(class_)

        @classmethod
        def get(class_, id):
            return pyramid_sqla.get_dbsession().query(class_).get(id)

    Base = declarative.declarative_base(cls=ORMClass)
    
    class User(Base):
        __tablename__ = "users"

        # Column definitions omitted

Then you can do things like this in your views::

    user_1 = models.User.get(1)
    q = models.User.query()

Whether this is a good thing or not depends on your perspective.
