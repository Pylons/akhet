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
        stats = psa.add_engine(settings, name="stats", prefix="stats.")
        # Can we retrieve the engines?
        self.assertIs(psa.get_engine(), default)
        self.assertIs(psa.get_engine("default"), default)
        self.assertIs(psa.get_engine("stats"), stats)
        # Are the session binding and base binding set correctly?
        self.assertIs(psa.get_session().bind, default)
        self.assertIs(psa.get_base().metadata.bind, default)

    def test_multiple_engines_without_default(self):
        settings = {
            "db1.url": self.db1.url,
            "db2.url": self.db2.url,
            "foo": "bar"}
        db1 = psa.add_engine(settings, name="db1", prefix="db1.")
        db2 = psa.add_engine(settings, name="db2", prefix="db2.")
        # Can we retrieve the engines?
        self.assertIs(psa.get_engine("db1"), db1)
        self.assertIs(psa.get_engine("db2"), db2)
        # There should be no default engine
        self.assertIs(psa.get_session().bind, None)
        self.assertIs(psa.get_base().metadata.bind, None)
        self.assertRaises(RuntimeError, psa.get_engine)

class TestDeclarativeBase(PyramidSQLATestCase):
    def test1(self):
        Base = psa.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        psa.add_engine(url=self.db1.url)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = psa.get_session()
        Session.configure(extension=None)  # XXX Kludge for SQLAlchemy/ZopeTransactionExtension bug
        sess = Session()
        sess.add_all([fred, wilma, barney, betty])
        sess.commit()
        sess.expunge_all()
        del fred, wilma, barney, betty
        # Can we get back a record?
        barney2 = sess.query(Person).get(3)
        self.assertEqual(barney2.id, 3)
        self.assertEqual(barney2.first_name, u"Barney")
        self.assertEqual(barney2.last_name, u"Rubble")
        sql = sa.select([Person.first_name])
        # Can we iterate the first names in reverse alphabetical order?
        q = sess.query(Person.first_name).order_by(Person.first_name.desc())
        result = [x.first_name for x in q]
        control = [u"Wilma", u"Fred", u"Betty", u"Barney"]
        self.assertEqual(result, control)

    def test1_with_ZopeTransactionExtension_bug(self):
        Base = psa.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        psa.add_engine(url=self.db1.url)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = psa.get_session()
        sess = Session()
        sess.add_all([fred, wilma, barney, betty])
        sess.commit()
        sess.expunge_all()
        del fred, wilma, barney, betty
        # Can we get back a record?
        barney2 = sess.query(Person).get(3)
        self.assertEqual(barney2.id, 3)
        self.assertEqual(barney2.first_name, u"Barney")
        self.assertEqual(barney2.last_name, u"Rubble")
        sql = sa.select([Person.first_name])
        # Can we iterate the first names in reverse alphabetical order?
        q = sess.query(Person.first_name).order_by(Person.first_name.desc())
        result = [x.first_name for x in q]
        control = [u"Wilma", u"Fred", u"Betty", u"Barney"]
        self.assertEqual(result, control)



