import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

_dbsession = None
_dbengines = {}

def _count_true(*items):
    true_items = filter(None, items)
    return len(true_items)

# PUBLIC API

__all__ = ["init_dbsession", "add_engine", "get_dbsession", "get_engine",
    "Base"]

Base = declarative_base()

def init_dbsession(settings=None, name="default", prefix="sqlalchemy.",
                    engine=None, bind_now=True, manage_transaction=True, 
                    sessionmaker_args=None, **engine_args):
    """
    """
    global _dbsession
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
            if isinstance(value, list):
                pass
            elif isinstance(value, tuple):
                value = list(value)
            else:
                value = [value]
            value.append(zte)
            sessionmaker_args["extension"] = value
        sm = orm.sessionmaker(**sessionmaker_args)
        _dbsession = orm.scoped_session(sm)
    if engine or settings or engine_args:
        e = add_engine(settings=settings, name=name, prefix=prefix, 
            engine=engine, **engine_args)
        _dbsession.configure(bind=e)
        Base.metadata.bind = e
    return _dbsession


def add_engine(settings=None, name="default", prefix="sqlalchemy.",
                    engine=None, **engine_args):
    """
    """
    if _count_true(settings, engine, engine_args) != 1:
        m = "only one of 'settings', 'engine', or '**engine_args' allowed"
        raise TypeError(m)
    if engine:
        e = engine
    elif settings:
        e = sa.engine_from_config(settings, prefix)
    else:
        e = sa.create_engine(**engine_args)
    _dbengines[name] = e
    return e


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

