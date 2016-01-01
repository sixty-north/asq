``asq.namedelements``
======================

.. automodule:: asq.namedelements

  ``IndexedElement``\s and ``KeyedElement`` are ``namedtuples`` useful for storing
  index, element pairs. They are used as the default selectors by the
  ``select_with_index()`` and ``select_many_with_index()``, ``select_with_correspondence()``
  and ``select_many_with_corresponding()`` query methods.


``asq.namedelements.IndexedElement``
------------------------------------

  .. autoclass:: IndexedElement

    The index and value of the element can be accessed via the ``index`` and ``value``
    attributes.

     .. automethod:: __new__(index, value)

     .. automethod:: __repr__()

     .. automethod:: __str__()


``asq.namedelements.KeyedElement``
----------------------------------

  .. autoclass:: KeyedElement

     The key and associated value can be accessed via the ``key`` and ``value``
     attributes.

     .. automethod:: __new__(key, value)

     .. automethod:: __repr__()

     .. automethod:: __str__()
