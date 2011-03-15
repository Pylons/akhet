Transaction manager
%%%%%%%%%%%%%%%%%%%

Akhet's SQALchemy configuration includes the pyramid_tm_ transaction manager.
This is a feature which TurboGears has long had but Pylons has not. The
transaction manager provides an automatic commit or rollback at the end of the
request processing, depending on whether an error has occurred.

(TurboGears uses a different transaction manager "repoze.tm2" which does
essentially the same thing but requires a middleware. pyramid_tm does not have
a middleware.)

.. _pyramid_tm: http://docs.pylonsproject.org/projects/pyramid_tm/dev/

How it works
============

After the view returns a response, a subscriber callback will automatically
commit all database changes in the Session unless an uncaught exception has
occurred, in which case it will roll back the changes. It will also roll back
the changes if the HTTP status is 4xx or 5xx. Finally, it clears the Session
for the next request.

You can still commit and roll back explicitly in your view, but you'll have to
use the ``transaction`` module instead of calling the Session methods
directly::

    import transaction
    transaction.commit()
    # Or:
    transaction.abort()

You may want to do this if you want to commit a lot of data a little bit at a
time.

You can also poison the transaction to prevent *any* database writes during this
request, including those performed by other parts of the application or
middleware. To do this, call::

    transaction.doom()

Of course, this doesn't affect changes that have already been committed.

The implementation is a combination of three packages that work together.
``transaction`` is a generic transaction manager. ``zope.sqlalchemy`` applies
this to SQLAlchemy by exposing a ``ZopeTransactionExtension``, which is a
SQLAlchemy session extension (a class that enhances the session's behavior).
``pyramid_tm`` takes care of issuing the commit or rollback at the end of the
request processing.

SQlAHelper maintains a ZopeTransactionExtension in the ``sqlahelper._zte``
variable. It automatically configures the Session to use that extension.

You can customize the circumstances under which an automatic rollback occurs by
defining a "commit veto" function. This is described in the pyramid_tm_
documentation.

Disabling the transaction manager
=================================

If you don't want managed transactions:

1. Delete the ``config.include("pyramid_tm")`` line in the ``main`` function.

2. Reconfigure the Session to not use the transaction extension::

        sqlahelper.get_session().config(extension=None)

If you disable the manager, you'll have to call
``Session.commit()`` or ``Session.rollback()`` yourself in your views. You'll
also have to configure the application to remove the session at the end of the
request. This would be in an event subscriber but I'm not sure which one.

Caveat: adding your own session extensions
==========================================

If you modify the ``extension`` session option in any way you'll lose the
transaction extension unless you re-add it. The extension lives in the
semi-private ``_zte`` variable in the library. Here's the proper way to add
your own extension while keeping the transaction extension::

    Session = sqlahelper.get_session()
    Session.configure(extension=[MyWonderfulExtension(), sqlahelper._zte])

Bypassing the transaction manager without disabling it
======================================================

In special circumstances you may want to do a particular database write while
allowing the transaction manager to roll back all other writes. For instance,
if you have a separate access log database and you want to log all responses,
even failures. In that case you can create a second SQLAlchemy session using
``sqlalchemy.orm.sessionmaker`` -- one that does *not* use the transaction
extension -- and use that session with that engine to insert and commit the log
record. 
