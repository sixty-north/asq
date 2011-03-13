``asq`` is simple implementation of a LINQ-inspired API for Python which operates over
Python iterables, including a parallel version implemented in terms of the
Python standard library multiprocessing module.

What It Does
============

``asq`` is a package implementing queries over iterables of Python
objects.  ``asq`` provides a fluent interface making extensive use of method
chaining to create complex queries without compromising readability.  Over 40
standard query operators are provided.

Requirements
============

This version of ``asq`` works with Python 2.6 and higher, including Python 3.
It has been tested on Python 2.6 and Python 3.2 and IronPython 2.6.

``asq`` has a dependency on the ``ordereddict`` module which ships as standard
with Python 2.7 and upwards, but this module must be installed separately
for Python 2.6.


