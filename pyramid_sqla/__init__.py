import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

# Global variables initialized by ``reset()``.
_base = _session = _engines = _zte = None

def reset():
    """Delete all engines and restore the initial module state.
    
    This function is mainly for unit tests and debugging. It undoes all
    customizations and reverts to the initial module state.
    """
    global _base, _session, _engines, _zte
    _zte = ZopeTransactionExtension()
    sm = orm.sessionmaker(extension=[_zte])
    _base = declarative.declarative_base()
    _session = orm.scoped_session(sm)
    _engines = {}

reset()

# PUBLIC API

__all__ = [
    "add_engine", 
    "config_session",
    "get_base",
    "get_session", 
    "get_engine",
    ]
    # "reset" is not included because it's not intended for normal use.

def add_engine(settings=None, name="default", prefix="sqlalchemy.",
    engine=None, **engine_args):
    """Configure a SQLAlchemy database engine and return it.

    I configure an engine in different ways depending on the combination of
    arguments. If ``name`` is not specified or its value is "default", I also
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

    * ``engine``: An existing SQLAlchemy engine. If you pass this you can't
      pass ``settings``, ``prefix``, or ``**engine_args``.

    * ``**engine_args``: Engine args supplied as keyword arguments. If
      ``settings`` is also passed, the keyword args override their
      corresponding settings. If ``settings`` is not passed, I call
      ``sqlalchemy.create_engine(**engine_args)`` directly.

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
    if engine and (settings or engine_args):
        m = "can't specify settings or engine args when ``engine`` is present"
        raise TypeError(m)
    elif engine:
        e = engine
    elif settings:
        if not prefix:
            raise ValueError("empty prefix ('') is not allowed")
        url_key = prefix + "url"
        if url_key not in settings and "url" not in engine_args:
            msg = """\
no database URL specified
settings key '%surl' is required when using prefix='%s'"""
            msg %= (url_key, prefix)
            if prefix and not prefix.endswith("."):
                msg += "\nHint: did you mean prefix='%s.'?" % prefix
            raise ValueError(msg)
        e = sa.engine_from_config(settings, prefix, **engine_args)
    else:
        try:
            url = engine_args.pop("url")
        except KeyError:
            raise TypeError("must pass settings dict or ``url`` keyword arg")
        e = sa.create_engine(url, **engine_args)
    _engines[name] = e
    if name == "default":
        _session.configure(bind=e)
        _base.metadata.bind = e
    return e

def get_session():
    """Return the central SQLAlchemy scoped session."""
    return _session

def get_engine(name="default"):
    """Return a database engine previously configured with ``add_engine``.

    If no argument, return the default engine. If an engine name is passed,
    return the engine that was registered under that name.

    Raise ``RuntimeError`` if no engine by that name was configured.
    """
    try:
        return _engines[name]
    except KeyError:
        raise RuntimeError("No engine '%s' was configured" % name)

def get_base():
    """Return the central declarative base.
    """
    return _base
