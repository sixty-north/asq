``asq.record``
==============

.. automodule:: asq.record

  Records provide a convenient anonymous class which can be useful for
  managing intermediate query results. ``new()`` provides a concise way to
  create ``Records`` in the middle of a query.

``asq.record.Record``
---------------------

  .. autoclass:: Record

     .. automethod:: __init__(**kwargs)

     .. automethod:: __repr__()

     .. automethod:: __getstate__()

     .. automethod:: __setstate__()

     .. automethod:: __str__()

``asq.record.new``
------------------

  .. autofunction:: new(**kwargs)

     .. rubric:: Example

     Create an employee and the get and set attributes::

       >>> employee = new(age=34, sex='M', name='Joe Bloggs', scores=[3, 2, 9, 8])
       >>> employee
       Record(age=34, scores=[3, 2, 9, 8], name='Joe Bloggs', sex='M')
       >>> employee.age
       34
       >>> employee.name
       'Joe Bloggs'
       >>> employee.age = 35
       >>> employee.age
       35


  