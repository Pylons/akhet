"""Akhet installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
CHANGES = open(os.path.join(here, "CHANGES.txt")).read()

requires = [
    "pyramid", 
    ]

entry_points = """
    [paste.paster_create_template]
    akhet=akhet.paster_templates:AkhetProjectTemplate
"""

setup(name="Akhet",
      version="1.0b1",
      description="Pyramid application templates inspired by Pylons 1.",
      long_description=README,
      #long_description=README + "\n\n" +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pylons",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        ],
      keywords="web wsgi pylons pyramid",
      author="Mike Orr",
      author_email="sluggoster@gmail.com",
      url="https://bitbucket.org/sluggo/akhet",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = requires,
      install_requires = requires,
      test_suite="akhet",
      entry_points=entry_points,
      )

