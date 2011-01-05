import os
import shutil
import tempfile
import unittest

import sqlalchemy as sa
from sqlalchemy.engine.base import Engine

import pyramid_sqla as psa

class DBInfo(object):
    def __init__(self, dir, filename):
        self.file = os.path.join(dir, filename)
        self.url = "sqlite:///" + self.file

class PyramidSQLATestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db1 = DBInfo(self.dir, "db1.sqlite")
        self.db2 = DBInfo(self.dir, "db2.sqlite")
        self.db3 = DBInfo(self.dir, "db3.sqlite")

    def tearDown(self):
        psa.reset()
        shutil.rmtree(self.dir, True)

    def assertDatabaseExists(self, db_file):
        self.assertEqual(os.path.exists(db_file), True)

    def assertDatabaseDoesNotExist(self, db_file):
        self.assertEqual(os.path.exists(db_file), False)

    if not hasattr(unittest.TestCase, "assertIsInstance"):
        def assertIsInstance(self, obj, classes):
            if not isinstance(obj, classes):
                typ = type(obj)
                if isinstance(classes, (list, tuple)):
                    classes_str = ", ".join(x.__name__ for x in classes)
                    classes_str = "[%s]" % classes_str
                else:
                    classes_str = classes.__name__
                msg = "%s is not an instance of %s" % (typ, classes_str)
                raise AssertionError(msg)

        def assertIs(self, a, b):
            if a is not b:
                raise AssertionError("%r is not %r" % (a, b))


class TestAddEngine(PyramidSQLATestCase):
    def test_keyword_args(self):
        engine = psa.add_engine(url=self.db1.url)
        self.assertIsInstance(engine, Engine)

    def test_simplest_settings(self):
        settings = {"sqlalchemy.url": self.db1.url}
        engine = psa.add_engine(settings, prefix="sqlalchemy.")
        self.assertIsInstance(engine, Engine)

    def test_existing_engine(self):
        e = sa.create_engine(self.db1.url)
        engine = psa.add_engine(engine=e)
        self.assertIs(engine, e)

    def test_multiple_engines(self):
        settings = {
            "sqlalchemy.url": self.db1.url,
            "stats.url": self.db2.url,
            "foo": "bar"}
        default = psa.add_engine(settings)
        stats = psa.add_engine(settings, name="stats", prefix="stats")

