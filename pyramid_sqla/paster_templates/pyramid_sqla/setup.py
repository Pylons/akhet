import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid>=1.0a10',
    'pyramid_beaker',
    'pyramid_handlers',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2>=1.0b1',  # default_commit_veto
    'zope.sqlalchemy',
    'WebError',
]

if sys.version_info[:3] < (2,5,0):
   requires.append('pysqlite')
    
entry_points = """\
    [paste.app_factory]
    main = {{package}}:main

    [paste.app_install]
    main = paste.script.appinstall:Installer
"""

setup(name='{{project}}',
      version='0.0',
      description='{{project}}',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="{{package}}",
      entry_points=entry_points,
      paster_plugins=['pyramid'],
      )

