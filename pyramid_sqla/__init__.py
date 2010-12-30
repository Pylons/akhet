import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

_base = None
_dbsession = None
_engines = {}

def _count_true(*items):
    true_items = filter(None, items)
    return len(true_items)

# PUBLIC API

__all__ = [
    "init_dbsession", 
    "add_engine", 
    "get_base",
    "get_dbsession", 
    "get_engine",
    ]

def init_dbsession(settings=None, prefix="sqlalchemy.",
    engine=None, manage_transaction=True, sessionmaker_args=None, 
    base_args=None, **engine_args):
    """Initialize the module for use.

    I do four things:

    1.  Configure a SQLAlchemy scoped session using ``sessionmaker_args``, and
        enable the ZopeTransactionExtension. The scoped session is available later
        by calling ``get_dbsession``.

    2. Configure a SQLAlchemy declarative base using ``base_args``. The base is
       available later by calling ``get_base``.
    
    3. If ``settings``, ``engine``, or ``**engine_args`` is specified, (A) call
       ``add_engine`` to configure a database engine and make it the default
       engine, (B) bind the engine to the session, and (C) bind the Base's
       metadata to the engine.  The engine is available later by calling
       ``get_engine``.

    4. Return the scoped session.

    Arguments:

    * ``settings``, ``prefix``, ``engine``, and ``**engine_args``: *(Optional)*
      See ``add_engine()``. (The engine name will be set to "default".)

    * ``manage_transaction``: *(Optional)* Pass false if you don't want the
      transaction extension.

    * ``sessionmaker_args``: *(Optional)* A dict of arguments for the
      sessionmaker constructor.

    * ``base_args``: *(Optional)* A dict of arguments for for the declarative base
      constructor. The most interesting arg is 'cls', which you can use to
      provide a common superclass to all ORM classes.

    Raise ``RuntimeError`` if the function is called more than once.
    """
    global _base, _dbsession
    if _dbsession:
        raise RuntimeError("database session is already configured")
    sm_args = _make_sessionmaker_args(sessionmaker_args, manage_transaction)
    sm = orm.sessionmaker(**sm_args)
    _dbsession = orm.scoped_session(sm)
    base_args = base_args or {}
    _base = declarative.declarative_base(**base_args)
    if engine or settings or engine_args:
        e = add_engine(settings=settings, prefix=prefix, engine=engine, 
            **engine_args)
        _dbsession.configure(bind=e)
        _base.metadata.bind = e
    return _dbsession


def add_engine(settings=None, name="default", prefix="sqlalchemy.",
    engine=None, **engine_args):
    """Configure a SQLAlchemy database engine and return it.

    I configure an engine in different ways depending on the combination of
    arguments.

    Arguments:

    * ``settings``: A dict of application settings (e.g., as parsed from an INI
      file), or a dict containing engine args. If this argument is passed, I call
      ``sqlalchemy.engine_from_config(settings, prefix)``.

    * ``name``: The engine name. This is used to retrieve the engine later. The
      default name is "default".

    * ``prefix``: If the keys in ``settings`` that pertain to this engine have
      a particular prefix, pass it here. This both chooses the keys that have
      this prefix, and strips the prefix from them to create the engine args.

    * ``engine``: An existing SQLAlchemy engine. 

    * ``**engine_args``: Engine args supplied as keyword arguments. If these
      arguments are passed, I call ``sqlalchemy.create_engine(**engine_args)``.

    You must pass exactly one of ``settings``, ``engine``, and
    ``**engine_args``; they are mutually exclusive. Raise
    ``RuntimeError`` if you pass none of them or too many.

    Examples::

        # The settings dict contains ``{"sqlalchemy.url": "mysql://..."}``
        engine = add_engine(settings, prefix="sqlalchemy.")

        # The settings dict contains ``{"url": "mysql://..."}
        engine = add_engine(settings)

        # Configure engine via keyword args
        engine = add_engine(url="mysql://...")

        # ``e`` is an existing SQLAlchemy engine
        engine = add_engine(e)
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
    _engines[name] = e
    return e


def get_dbsession():
    """Return the central SQLAlchemy scoped session.

    Raise ``RuntimeError`` if ``init_dbsession`` has not been called.
    """
    if _dbsession is None:
        raise RuntimeError("``init_dbsession`` has not been called")
    return _dbsession

def get_engine(name="default"):
    """Return a database engine.

    If no argument, return the default engine that was specified with
    ``init_dbsession``. If an engine name is passed, return the engine that was
    registered with ``add_engine`` under that name.

    Raise ``RuntimeError`` if ``init_dbsession`` hasn't been called or no
    engine by that name was initialized.
    """
    try:
        return _engines[name]
    except KeyError:
        raise RuntimeError("No engine '%s' was configured" % name)

def get_base():
    """Return the central declarative base.

    Raise ``RuntimeError`` if ``init_dbsession`` has not been called.
    """
    if _base is None:
        raise RuntimeError("``init_base`` has not been called")
    return _base

#### Private functions

def _make_sessionmaker_args(user_sm_args, manage_transaction):
    if user_sm_args is not None:
        sm_args = user_sm_args.copy()
    else:
        sm_args = {}
    if manage_transaction:
        zte = ZopeTransactionExtension()
        # This part is tricky because there may or may not be an existing
        # 'extension' key, and its value may be a list or a single object.
        # Convert all forms to a list and append the transaction 
        # extension.
        value = sm_args.get("extension", [])
        if isinstance(value, list):
            pass
        elif isinstance(value, tuple):
            value = list(value)
        else:
            value = [value]
        value.append(zte)
        sm_args["extension"] = value
    return sm_args
