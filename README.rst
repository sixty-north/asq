``asq`` is simple implementation of a LINQ-inspired API for Python which
operates over Python iterables, including a parallel version implemented in
terms of the Python standard library multiprocessing module.

What It Does
============

``asq`` is a package implementing queries over iterables of Python
objects.  `asq` provides a fluent interface making extensive use of method
chaining to create complex queries without compromising readability.  For
example, to take the first five uppercased results from a list of words sorted
by length and then alphabetically, try::

  >>> from asq import query
  >>> words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
  >>> query(words).order_by(len).then_by().take(5).select(str.upper).to_list()
  ['ONE', 'SIX', 'TEN', 'TWO', 'FIVE']

Over 40 standard query operators are provided together with various utilities
to make the API even more convenient to use in Python.

Status
======

Build status:

.. image:: https://travis-ci.org/sixty-north/segpy.svg?branch=master
    :target: https://travis-ci.org/sixty-north/segpy
    :alt: Build Status

.. image:: https://readthedocs.org/projects/asq/badge/?version=latest
    :target: https://readthedocs.org/projects/asq/?badge=latest
    :alt: Documentation Status

How to get it
=============

``asq`` is available on the Python Package Index and can be installed with
easy_install from setuptools::

  $ pip install asq

Alternatively you can download and unpack the source and install using::

  $ cd asq-1.0
  $ python setup.py install

Requirements
============

This version of ``asq`` works with Python 2.6 and higher, including Python 3.
It has been tested on Python 2.6, Python 2.7, Python 3.1 and Python 3.2, 3.3
and 3.4. Furthermore it is tested on IronPython 2.6 and IronPython 2.7.

``asq`` has a dependency on the ordereddict module which ships as standard
with Python 2.7 and upwards, but this module must be installed separately
for Python 2.6.

