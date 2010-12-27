Model examples
==============

This chapter gives some examples for writing your application models. These are
based on the `SQLAlchemy documentation`_, which should be your primary guide.

These models assume SQLAlchemy 0.6.x and Python >= 2.6. For earlier versions of
Python, use the ``%`` operator instead of the the string ``.format`` method.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/

A simple one-table model
------------------------

    import pyramid_sqla as psa
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    class User(psa.Base):
        __tablename__ = "users"

        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.Unicode(100), nullable=False)
        email = sa.Column(sa.Unicode(100), nullable=False)

This model has one ORM class, ``User`` corresponding to a database table
``users``. The table has three columns: ``id``, ``name``, and ``user``.  ::


A three-table model
-------------------

We can expand the above into a three-table model suitable for a medium-sized
application. (This example uses the string ``.format`` method introduced in
Python 2.6. In older versions, use the ``%`` operator instead.) ::

    import pyramid_sqla as psa
    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    class User(psa.Base):
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
            q = psa.get_dbsession().query(User)
            q = q.order_by(User.name)
            return q
        

    class Address(psa.Base):
        __tablename__ = "addresses"

        id = sa.Column(sa.Integer, primary_key=True)
        user_id = foreign_key_column(None, sa.Integer, "users.id"),
        street = sa.Column(sa.Unicode(40), nullable=False)
        city = sa.Column(sa.Unicode(40), nullable=False)
        state = sa.Column(sa.Unicode(2), nullable=False)
        zip = sa.Column(sa.Unicode(10), nullable=False)
        country = sa.Column(sa.Unicode(40), nullable=False)
        foreign_extra = sa.Column(sa.Unicode(100, nullable=False)

        def __str__(self):
            """Return the address as a string formatted for a mailing label."""
            state_zip = u"{0} {1}".format(self.state, self.zip).strip()
            cityline = filterjoin(u", ", self.city, state_zip)
            lines = [self.street, cityline, self.foreign_extra, self.country]
            return filterjoin(u"|n", *lines) + u"\n"


    class Activity(psa.Base):
        __tablename__ = "activities"

        id = sa.Column(sa.Integer, primary_key=True)
        activity = sa.Column(sa.Unicode(100), nullable=False)


    assoc_users_activities = sa.Table("assoc_users_activities", psa.Base.metadata,
        foreign_key_column("user_id", sa.Integer, "users.id"),
        foreign_key_column("activities_id", sa.Unicode(100), "activities.id"))
            

     # Utility functions
     def filterjoin(sep, *items):
        """Join the items ianto a string, dropping any that are empty.
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
``Address`` class with an ``addresses`` table, and an ``Activity``
class with ``activities`` table.  ``users`` is in a 1:Many relationship with
``addresses``.  ``users`` is also in a Many:Many`` relationship with
``activities`` using the association table ``assoc_users_activities``.
This is the SQLAlchemy "declarative" syntax, which defines the tables in terms of
ORM classes subclassed from a declarative ``Base`` class. Association tables do
not have an ORM class in SQLAlchemy, so we define it using the ``Table``
constructor as if we weren't using declarative, but it's still tied to the
Base's "metadata".

We can add instance methods to the ORM classes and they will be valid for one
database record, as with the ``Address.__str__`` method. We can also define
class methods that operate on several records or return a query object, as with
the ``User.by_name`` method. 

Inside the class method we refer to the table by its proper name (``User``),
althogh if would be more usual in class methods to use the ``class_`` argument.
This is a personal preference: it's easier to read the module code if ORM
classes are always called the same name. We could have used a static method
since we're not using the ``class_`` argument anywhere, but again it's
customary to use class methods. That doesn't mean class methods are necessarily
better than static methods, however, it's just what we're used to.

Initializing the database
-------------------------
