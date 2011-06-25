#! /usr/bin/env python

"""Distutils setup file."""

from distutils.core import setup
import playwhe

readme = open("README", "r")
long_description = readme.read()
readme.close()

setup(name="playwhe",
      version=playwhe.__version__,
      description="A Python API and script for retrieving Play Whe results.",
      long_description=long_description,
      url="http://pypi.python.org/pypi/playwhe",
      license="License :: Public Domain",
      author=playwhe.__author__,
      author_email=playwhe.__email__,
      py_modules=["playwhe"],
      scripts=["playwhe.py"],
      classifiers=["Development Status :: 3 - Alpha",
                   "License :: Public Domain",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: Unix",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries"]
)
