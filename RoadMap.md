# Planned versions #

In reverse chronological order (most recent first)

## asq 3.0 ##

  * Expression tree based implementation.
  * Pluggable asq providers asq-for-XML, asq-for-XML.  To be decided...

## asq 2.0 ##

  * Parallel execution support equivalent to PLINQ.

## asq 1.1 ##

  * Implementation of additional operators, including common extensions equivalent to those provided by projects such as [morelinq](http://code.google.com/p/morelinq/) or the various recipes commonly used with Python itertools.
  * Implementation of lazy rich comparisons between sequences.
  * Add `kq_`, `aq_` and `mq_` selector factories which wrap Queryables around the selector return value.
  * If a selector or predicate is passed as a string, manufacture the appropriate attribute or method-call selector depending on whether the attribute is callable or not. This could make many queries more concise.
  * Consider allowing order\_by() and then\_by() accept multiple selectors.
  * Support for Queryable slicing.
  * Beta quality support for parallel execution.

# Historical versions #

## asq 1.0 ##

**Released: 2011-Jun-05**

  * Complete API documentation.
  * Examples.
  * PEP8 compliance
  * Convenience selector factories
  * Convenience predicate factories and combinator factories
  * Record type and factory for anonymous objects.
  * Debugging support through logging.
  * Alpha quality support for parallel query execution.

## asq 0.9 ##

**Released: 2011-Mar-14**

  * Complete equivalence with LINQ for Objects on .NET 4.
  * Serial (_i.e._ non-parallel) execution.
  * 100% test coverage.
  * Full support for Python 2.6 through to Python 3.2 including IronPython.
  * Present on the Python Package Index (PyPI) and available through easy\_install, pip or other such tools.
  * Alpha quality support for parallel execution.

## asq 0.5 ##

**Released: 2011-Jan-13**

  * The prototype.  Incomplete. Buggy. Undocumented. Proof of concept.