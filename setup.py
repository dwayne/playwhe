#!/usr/bin/env python

"""Distutils setup file."""

from distutils.core import setup

setup(name="playwhe",
      version="0.2a1",
      description="A Python API for retrieving Play Whe results.",
      url="http://pypi.python.org/pypi/playwhe",
      license="License :: Public Domain",
      author="Dwayne R. Crooks",
      author_email="me@dwaynecrooks.com",
      py_modules=["playwhe"],
      classifiers=["Development Status :: 3 - Alpha",
                   "License :: Public Domain",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: Unix",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries"],
      long_description="""\
This library provides a Python interface for retrieving Play Whe
results from the `National Lotteries Control Board <http://www.nlcb.co.tt/>`_
(NLCB) website.

Example usage::

    from playwhe import Mark, PlayWhe
    
    p = PlayWhe()
    
    # retrieve all the results for the month of April in the year 2011
    for r in p.results_for_month(2011, 4):
        print r
    
    # retrieve the results for April 2nd, 2011
    for r in p.results_for_day(2011, 4, 2):
        print r
    
    # retrieve the two most recent results
    for r in p.results():
        print r
    
    # display the standard names associated with each number
    for n in range(Mark.lowest, Mark.highest + 1):
        print "%2d - %s" % (n, Mark.get_name_of_number(n))

""")
