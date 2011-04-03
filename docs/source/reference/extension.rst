Extension
==========

.. automodule:: asq.extension

  The ``extension`` modules contains tools for registering new extension
  operators with ``asq``. This is achieved by dynamically adding new methods to
  ``Queryable`` and possibly its subclasses.

  .. autosummary::
     :nosignatures:

     .. currentmodule asq.extension

     add_method
     extend

  .. autofunction:: add_method(function, klass, name=None)

     .. rubric:: Example

     Define a function called ``every_second()`` which returns every second
     element from the source and add it to ``Queryable`` as a new query
     operator called ``alternate()``::

       >>> def every_second(self):
       ...     def generate():
       ...         for index, item in enumerate(self):
       ...             if index % 2 == 0:
       ...                 yield item
       ...     return self._create(generate())
       ...
       >>> from asq.extension import add_method
       >>> from asq.queryables import Queryable
       >>>
       >>> add_method(every_second, Queryable, "alternate")
       <function every_second at 0x0000000002D2D5C8>
       >>> a = [5, 8, 3, 2, 0, 9, 5, 4, 9, 2, 7, 0]
       >>> query(a).alternate().to_list()
       [5, 3, 0, 5, 9, 7]

  .. autofunction:: extend(klass, name=None)

     .. rubric:: Example

     Define a new query method called ``pairs()`` which iterates over
     successive pairs in the source iterable, add it to the ``Queryable``
     class and use it to execute a query.  Note that extension methods
     defined in this way will typically need to call internal methods of
     ``Queryable``, such as the ``_create()`` method used here to construct a
     new ``Queryable``::

       >>> from asq.extension import extend
       >>> from asq.queryables import Queryable
       >>>
       >>> @extend(Queryable)
       ... def pairs(self):
       ...     def generate_pairs():
       ...         i = iter(self)
       ...         sentinel = object()
       ...         prev = next(i, sentinel)
       ...         if prev is sentinel:
       ...             return
       ...         for item in i:
       ...             yield prev, item
       ...             prev = item
       ...     return self._create(generate_pairs())
       ...
       >>> from asq.initiators import query
       >>> a = [5, 4, 7, 2, 8, 9, 1, 0, 4]
       >>> query(a).pairs().to_list()
       [(5, 4), (4, 7), (7, 2), (2, 8), (8, 9), (9, 1), (1, 0), (0, 4)]