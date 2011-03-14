# Asq's setup.py

from distutils.core import setup

from asq import __version__ as version

with open('README.txt', 'r') as readme:
    long_description = readme.read()

setup(
    name = "asq",
    packages = ["asq"],
    version = "{version}".format(version=version),
    description = "LINQ-for-objects style queries for Python iterables.",
    author = "Robert Smallshire",
    author_email = "robert@smallshire.org.uk",
    url = "http://code.google.com/p/asq/",
    download_url="http://code.google.com/p/asq/downloads/detail?name=asq-{version}.tar.gz".format(version=version),
    keywords = ["Python", "LINQ"],
    license="MIT License",
    classifiers = [
        "Development Status :: 4 - Beta"
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6"
        "Programming Language :: Python :: 2.7"
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        "Topic :: Utilities",
        ],
    requires = ['ordereddict'],
    long_description = long_description
)
