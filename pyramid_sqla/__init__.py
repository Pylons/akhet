
import sqlalchemy as sa
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

_dbsession = None
_dbengines = {}

def init_dbsession(settings=None, name="default", prefix="sqlalchemy.",
                    engine=None, bind_now=True, manage_transaction=True, 
                    sessionmaker_args=None, **engine_args):
    """
    By default the dbsession is managed by ``ZopeTransactionSession``. This
    means that if your application is wrapped in the ``repoze.tm2`` middleware,
    it will automatically commit at the end of every request unless an uncaught
    exception has occurred, in which case it will rollback. You can explicitly
    commit in your view via ``import transaction; transaction.commit()``.
    (``transaction`` is a top-level module which is a dependency of
    ``repoze.tm2``.) To rollback, call ``transaction.abort()``.  To prevent
    *any* database writes during this request, including any performed by other
    parts of the application, call ``transaction.doom()``.

    If you don't want managed transactions at all, pass
    ``manage_transaction=False`` to ``init_dbsession``, and do *not* wrap your
    application in the ``repoze.tm2`` middleware. In this case you must use
    ``dbsession.commit()`` 

    """
    global _dbsession
    if engine:
        pass
    elif settings:
        engine = sa.engine_from_config(settings, prefix)
    else:
        engine = sa.create_engine(**engine_args)
    _dbengines[name] = engine
    if _dbsession is None:
        if sessionmaker_args is not None:
            sessionmaker_args = sessionmaker_args.copy()
        else:
            sessionmaker_args = {}
        if manage_transaction:
            zte = ZopeTransactionExtension()
            # This part is tricky because there may or may not be an existing
            # 'extension' key, and its value may be a list or a single object.
            value = sessionmaker_args.get("extension", [])
            if not isinstance(value, (list, tuple)):
                value = [value]
            value.append(zte)
            sessionmaker_args["extension"] = value
        sm = orm.sessionmaker(**sessionmaker_args)
        _dbsession = orm.scoped_session(sm)
    if bind_now:
        _dbsession.configure(bind=engine)
    return _dbsession

def get_dbsession():
    """Return a SQLAlchemy scoped session for use in models, views, etc.

    See
    http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
    for more details on scoped sessions.
    """
    global _dbsession
    if _dbsession is None:
        raise RuntimeError("no database sessions configured")
    return _dbsession

def get_dbengine(name="default"):
    try:
        return db_engines[name]
    except KeyError:
        raise RuntimeError("No engine '%s' was configured" % name)

