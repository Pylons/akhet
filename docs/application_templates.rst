Application template details
============================

For a simple Pyramid application with one database engine, follow these steps:

1. Add it to your list of 'requires' dependencies in *setup.py*.

2. In your *development.ini* file add:

   .. code-block:: ini

        sqlalchemy.url = sqlite:///%(here)s/db.sqlite

   You can also add any SQLALchemy engine options such as:

    .. code-block:: ini

        sqlalchemy.pool_recycle = 3600
        sqlalchemy.convert_unicode = true

3. Add the repoze.tm2 middleware to the pipeline:

   .. code-block:: ini

        [pipeline:main]
        pipeline =
            egg:WebError#evalerror
            egg:repoze.tm2#tm
            MyApp

    (Replace "myapp" with your application name, corresponding to the
    "[app:myapp]" section.)

4.  To log SQL queries, modify the "[logger_sqlalchemy]" section in
    *development.ini*. Set ``level = INFO`` to log all queries, ``level =
    DEBUG`` to log queries and results (very verbose!), or ``level = WARN`` to
    log neither. If your *development.ini* does not have a
    "[logger_sqlalchemy]" section, create a new Pyramid application and copy
    all the logging sections from its *development.ini*.

5. In *myapp/__init__.py*, add the following at the top::

        import pyramid_sqla

   Then inside the ``main()`` function, add this like::

        pyramid_sqla.init_dbsession(settings, prefix="sqlalchemy.")

6. In models or views or anywhere else you need them::

        import pyramid_sqla

        Session = pyramid_sqla.get_dbsession()
        engine = pyramid_sqla.get_dbengine()

Note that ``get_dbsession()`` returns a SQLAlchemy scoped session
not a plain SQLAlchemy session.
