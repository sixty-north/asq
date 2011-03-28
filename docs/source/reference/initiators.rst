Initiators
==========

.. automodule:: asq.initiators

  Initiators are so-called because they are used to initiate a query expression
  using the fluent interface of ``asq`` which uses method-chaining to compose
  complex queries from the query operators provided by queryables.

  .. autosummary::
     :nosignatures:

     .. currentmodule asq.initiators

     asq
     empty
     integers
     repeat

  .. autofunction:: asq(iterable)

     .. rubric:: Examples

     Create a queryable from a list::

       >>> from asq.initiators import asq
       >>> a = [1, 7, 9, 4, 3, 2]
       >>> q = asq(a)
       >>> q
       Queryable([1, 7, 9, 4, 3, 2])
       >>> q.to_list()
       [1, 7, 9, 4, 3, 2]

  .. autofunction:: empty()

     .. rubric:: Examples

     Create a queryable from a list::

       >>> from asq.initiators import empty
       >>> q = empty()
       >>> q
       Queryable(())
       >>> q.to_list()
       []

     See that ``empty()`` always returns the same instance::

       >>> a = empty()
       >>> b = empty()
       >>> a is b
       True

  .. autofunction:: integers(start, count)

     .. rubric:: Examples

     Create the first five integers::

       >>> from asq.initiators import integers
       >>> numbers = integers(0, 5)
       >>> numbers
       Queryable(range(0, 5))
       >>> numbers.to_list()
       [0, 1, 2, 3, 4]

  .. autofunction:: repeat(element, count)

    .. rubric:: Examples

    Repeat the letter x five times::

      >>> from asq.initiators import repeat
      >>> q = repeat('x', 5)
      >>> q
      Queryable(repeat('x', 5))
      >>> q.to_list()
      ['x', 'x', 'x', 'x', 'x']