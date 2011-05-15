#!/usr/bin/env python

"""Distutils setup file."""

from distutils.core import setup

setup(name="playwhe",
      version="0.1",
      description="A Python API for retrieving Play Whe results.",
      url="http://pypi.python.org/pypi/playwhe/0.1",
      license="License :: Public Domain",
      author="Dwayne R. Crooks",
      author_email="me@dwaynecrooks.com",
      py_modules=["playwhe"],
      classifiers=["Development Status :: 4 - Beta",
                   "License :: Public Domain",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: Unix",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries"],
      long_description="""\
This library provides a pure Python interface for retrieving Play Whe
results from the `National Lotteries Control Board <http://www.nlcb.co.tt/>`_
(NLCB) website.

Example usage::

    import playwhe
    
    p = playwhe.PlayWhe()
    
    # retrieve all the results for the month of April in the year 2011
    r = p.results_for_month(2011, 4)
    
    # retrieve the results for April 2nd, 2011
    r = p.results_for_day(2011, 4, 2)
    
    # retrieve the two most recent results
    r = p.results()
    
    # display the standard names associated with each mark
    for mark in range(playwhe.LOWEST_MARK, playwhe.HIGHEST_MARK + 1):
        print "%2d - %s" % (mark, playwhe.name_of_mark(mark))

""")
