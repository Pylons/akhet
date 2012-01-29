"""Akhet installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
README = README.split("\n\n", 1)[0] + "\n"
CHANGES = open(os.path.join(here, "CHANGES.txt")).read()

requires = [
    "pyramid", 
    ]

entry_points = """
"""

setup(name="Akhet",
      version="2.0",
      description="A Pyramid library and demo app with a Pylons-inspired API.",
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

