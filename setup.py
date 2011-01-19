# Asq's setup.py

from distutils.core import setup
setup(
    name = "asq",
    packages = ["asq"],
    version = "0.5",
    description = "LINQ-for-objects inspired implementation for Python",
    author = "Robert Smallshire",
    author_email = "robert@smallshire.org.uk",
    url = "http://code.google.com/p/asq/",
    keywords = ["Python", "LINQ", "Parallel"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2"
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        "Topic :: Utilities",
        ],
    long_description = """\
Asq
===

A simple implementation of a LINQ-inspired API for Python which operates over
Python iterables, including a parallel version implemented in terms of the
Python standard library multiprocessing module.
"""
)
