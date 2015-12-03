``asq.indexedelement``
======================

.. automodule:: asq.indexedelement

  ``IndexedElement``\s are ``namedtuples`` useful for storing index, element pairs.
  They are used as the default selectors by the ``select_with_index()`` and
  ``select_many_with_index()`` query methods.  The index and element can be accessed
  via the ``index`` and ``element`` attributes or via the zero and one indexes
  respectively.

``asq.indexedelement.IndexedElement``
-------------------------------------

  .. autoclass:: IndexedElement

     .. automethod:: __new__(index, element)

     .. automethod:: __repr__()

     .. automethod:: __str__()



