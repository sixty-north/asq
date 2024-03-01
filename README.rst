*Asq* is simple implementation of a LINQ-inspired API for Python which
operates over Python iterables, including a parallel version implemented in
terms of the Python standard library multiprocessing module.

What It Does
============

*Asq* is a package implementing queries over iterables of Python
objects. *Asq* provides a fluent interface making extensive use of method
chaining to create complex queries without compromising readability.  For
example, to take the first five uppercased results from a list of words sorted
by length and then alphabetically, try::

  >>> from asq import query
  >>> words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
  >>> query(words).order_by(len).then_by().take(5).select(str.upper).to_list()
  ['ONE', 'SIX', 'TEN', 'TWO', 'FIVE']

Over 40 standard query operators are provided together with various utilities
to make the API even more convenient to use in Python.

Documentation
=============

Of course, there is full `Narrative and reference documentation for asq <http://asq.readthedocs.org/>`_

Status
======

Build status:

.. image:: https://github.com/sixty-north/asq/workflows/actions.yml/badge.svg
    :alt: Build Status

.. image:: https://readthedocs.org/projects/asq/badge/?version=latest
    :target: https://readthedocs.org/projects/asq/?badge=latest
    :alt: Documentation Status

How to get it
=============

*Asq* is available on the Python Package Index and can be installed with ``pip``::

  $ pip install asq

Requirements
============

This version of *Asq* works with Python 3.9 and higher
