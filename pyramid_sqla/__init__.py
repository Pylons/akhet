import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

# Global variables initialized by ``reset()``.
_base = _dbsession = _engines = _zte = None

def reset():
    """Restore initial module state.
    
    This function is mainly for unit tests and debugging. It deletes all
    engines and recreates the dbsession and other global objects.
    """
    global _base, _dbsession, _engines, _zte
    _zte = ZopeTransactionExtension
    sm = orm.sessionmaker(extension=[_zte])
    _base = declarative.declarative_base()
    _dbsession = orm.scoped_session(sm)
    _engines = {}

reset()

# PUBLIC API

__all__ = [
    "add_engine", 
    "config_dbsession",
    "get_base",
    "get_dbsession", 
    "get_engine",
    ]
    # "reset" is not included because it's not intended for normal use.

def add_engine(settings=None, name="default", prefix="sqlalchemy.",
    engine=None, **engine_args):
    """Configure a SQLAlchemy database engine and return it.

    I configure an engine in different ways depending on the combination of
    arguments. If ``name`` is not specified or the value is "default", I also
    bind the scoped session and the declarative base's metadata to it.

    Arguments:

    * ``settings``: A dict of application settings (e.g., as parsed from an INI
      file), or a dict containing engine args. If this argument is passed, I
      call ``sqlalchemy.engine_from_config(settings, prefix)``.

    * ``name``: The engine name. This is used to retrieve the engine later. The
      default name is "default".

    * ``prefix``: This is used with ``settings`` to calcuate the engine args.
      The default value is "sqlalchemy.", which tells SQLAlchemy to use the
      keys starting with "sqlalchemy." for this engine.

    * ``engine``: An existing SQLAlchemy engine. 

    * ``**engine_args``: Engine args supplied as keyword arguments. If these
      arguments are passed, I call ``sqlalchemy.create_engine(**engine_args)``.

    You must pass exactly one of ``settings``, ``engine``, and
    ``**engine_args``. Raise ``RuntimeError`` if you pass none of them or too
    many.

    SQLAlchemy will raise a ``KeyError`` if the database URL is not specified.
    This may indicate the settings dict has no "PREFIX.url" key or that the
    ``url`` keyword arg was not passed.

    Examples::

        # Configure engine using a settings dict
        settings = {"sqlalchemy.url": "mysql://..."}
        engine = add_engine(settings, prefix="sqlalchemy.")

        # Configure engine via keyword args
        engine = add_engine(url="mysql://...")

        # ``e`` is an existing SQLAlchemy engine
        engine = add_engine(e)

        # Configure two engines, the first one as default
        settings = {"db1.url": "mysql://...", "db2.url": "postgresql://..."})
        engine1 = add_engine(settings, prefix="db1.")
        engine2 = add_engine(settings, name="stats", prefix="db2.")

        # Configure two engines with no default engine
        settings = {"db1.url": "mysql://...", "db2.url": "postgresql://..."})
        engine1 = add_engine(settings, name="engine1", prefix="db1.")
        engine2 = add_engine(settings, name="engine2", prefix="db2.")
    """
    if _count_true(settings, engine, engine_args) != 1:
        m = "only one of 'settings', 'engine', or '**engine_args' allowed"
        raise TypeError(m)
    if engine:
        e = engine
    elif settings:
        e = sa.engine_from_config(settings, prefix)
    else:
        try:
            url = engine_args.pop("url")
        except KeyError:
            raise TypeError("must pass settings dict or ``url`` keyword arg")
        e = sa.create_engine(url, **engine_args)
    _engines[name] = e
    if name == "default":
        _dbsession.configure(bind=e)
        _base.metadata.bind = e
    return e

def config_dbsession(**sessionmaker_args):
    """Reconfigure the scoped session.

    ``**sessionmaker_args`` may be any ``sessionmaker`` arguments. Arguments
    not specified will remain at their previous state.
    
    If the ``extension`` arg is given, it must be a list of extensions (not a
    single extension) and must NOT include a ``ZopeTransactionExtension``. Note
    that this is more restrictive than the corresponding ``sessionmaker`` arg.
    """
    sm_args = sessionmaker_args
    if "extension" in sm_args:
        ext = list(sm_args["extension"])
        ext.append(_zte)
    else:
        ext = [_zte]
    sm_args["extension"] = ext
    _dbsession.configure(**sm_args)

def get_dbsession():
    """Return the central SQLAlchemy scoped session.
    """
    return _dbsession

def get_engine(name="default"):
    """Return a database engine that was previously configured with ``add_engine``.

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
    """
    return _base

#### Private functions

def _count_true(*items):
    """Return a count of true items in ``*items``.
    """
    true_items = filter(None, items)
    return len(true_items)

