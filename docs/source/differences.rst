Differences from LINQ
=====================

Although ``asq`` is inspired by LINQ, there are inevitably some differences
with Microsoft's LINQ on .NET in order to accommodate the variance between C#
and Python.

Embedded Domain Specific Language
---------------------------------

C# and VB.NET have specific syntax extensions to support the creation of LINQ
queries. This provides an alternative to the fluent interface (method
chaining).  Any LINQ query can be expressed using the fluent interface. This is
not true for the LINQ domain specific languages embedded in C# and VB.NET but
they provide syntactic sugar for many common queries structures.

For example the following LINQ comprehension expression in C#:

.. code-block:: c#

   from item in collection where item.id == 3 select item

is equivalent to the following call without syntactic sugar in C#:

.. code-block:: c#

   collection.Where(item => item.id == 3)

No language extensions are provided by ``asq``; however, the fluent
interface is fully supported.

``let`` bindings
----------------

LINQ query syntax includes a ``let`` keyword which has no direct equivalent in
the LINQ fluent (method chaining) interface.  The ``let`` keyword introduces a
new identifier which can store intermediate query results for improvements in
readability or performance.

All queries in LINQ syntax are translated by the C# compiler into chained
method calls. The ``let`` keyword is translated into a ``select()`` mapping
which creates instances of anonymous types which bundle together the current
query value together with any addition values bound by ``let`` so they may all
be passed down the method chain. Selectors and predicates in the method chain
following the ``select()`` are modified to extract the correct members from the
anonymous type.

For example, the following LINQ query expression::

  var names = new string[] { "Dog", "Cat", "Giraffe", "Monkey", "Tortoise" };
  var result =
      from animalName in names
      let nameLength = animalName.Length
      where nameLength > 3
      orderby nameLength
      select animalName;

is equivalent to the C# method chain:

.. code-block:: c#

   var result = names
       .Select(animalName => new { nameLength = animalName.Length, animalName})
       .Where(x=>x.nameLength > 3)
       .OrderBy(x=>x.nameLength)
       .Select(x=>x.animalName);

The latter form can be emulated in ``asq`` using a ``Record`` object which can
be concisely created by the ``new()`` factory function::

  from asq.initiators import asq
  from asq.record import new

  names = ['Dog', 'Cat', 'Giraffe', 'Monkey', 'Tortoise']
  result = query(names)
      .select(lambda animal_name: new(name_length=len(animal_name),
                                      animal_name=animal_name))
      .where(lambda x: x.name_length > 3)
      .order_by(lambda x: x.name_length)
      .select(lambda x: x.animal_name)

Extension methods
-----------------

C# supports extension methods which allow LINQ to "add" methods to existing
types such as ``IEnumerable``. This is how the LINQ query operators are added
to enumerable types.  Python has no fully equivalent technique because so-
called monkey patching, whereby new methods can be added to existing classes,
cannot be applied to built-in types such as list because they are immutable by
design.

For this reason query initiators such ``query()`` must be used to convert a
Python iterable into a type which supports query operators.

Nonetheless, the core operators included in ``asq`` may be supplemented with
additional operators by adding new methods to the appropriate queryable type,
usually ``Queryable`` itself.

A decorator called ``@extend`` is provided by ``asq`` for this purpose.

Overloading
-----------

Being statically typed C# supports method overloading and this is used
extensively by LINQ. For example, the ``SelectMany()`` method has the following
four overloads:

.. code-block:: c#

  SelectMany<TSource, TResult>(IEnumerable<TSource>,
                               Func<TSource, IEnumerable<TResult>>)

  SelectMany<TSource, TResult>(IEnumerable<TSource>,
                               Func<TSource, Int32, IEnumerable<TResult>>)

  SelectMany<TSource, TCollection, TResult>(IEnumerable<TSource>,
                                            Func<TSource, IEnumerable<TCollection>>,
                                            Func<TSource, TCollection, TResult>)

  SelectMany<TSource, TCollection, TResult>(IEnumerable<TSource>,
                                            Func<TSource, Int32, IEnumerable<TCollection>>,
                                            Func<TSource, TCollection, TResult>)

These four overloads perform quite distinct, although related, operations.  In
``asq`` the equivalent of these overloads are methods with separate - and more
descriptive - names::

  select_many(collection_selector, result_selector)

  select_many_with_index(collection_selector, result_selector)

  select_many_with_correspondence(collection_selector, result_selector)

Default arguments allow the Python ``select_many()`` method to perform the
equivalent function as the first and third C# overloads and
``select_many_with_index()`` the second and fourth overloads.  The third Python
method provides a simpler alternative to the second version in some scenarios.

Equality comparers
------------------

Many .NET containers and and LINQ operators allow the specification of
comparer objects, particularly IEqualityComparer. This is important in C#
because equality in C# using the equality operator is by reference rather than
value.  The use of separate comparer types is not idiomatic in Python and in
general no attempt has been made to support the equivalent of LINQ operator
overloads which accept equality comparers.

Two ``asq`` operators which *do* accept equality comparison functions are
``contains()`` and ``sequence_equal()``.

Style changes
-------------

All class and method names in ``asq`` are compatible with the PEP 8 style-
guide.  This necessarily requires that they are different to the .NET methods,
so, for example, ``SelectMany()`` in .NET becomes ``select_many()`` in ``asq``.

The LINQ IEnumerable extension methods which create new sequences rather than
operate on existing sequences have become module-scope free function
*initiators* in ``asq`` in the ``initiators`` sub-module.

Specific naming changes
-----------------------

Owing to clashes with existing Python types, some specific name changes have
been made. Other name changes have been made because overloads in LINQ have
become separate named methods in ``asq``.

 =============== ===================
 LINQ            `asq`
 =============== ===================
 ``IEnumerable`` ``query(iterable)``
 ``range()``     ``integers()``
 ``except()``    ``difference()``
 =============== ===================

Selector and predicate factories
--------------------------------

Lambdas in Python are relatively verbose compared to C# lambdas and have the
further restriction that they cannot span multiple lines.  Selector and
predicate factories are provided to ``asq`` to generate common lambda forms.
These have some out-of-the-box equivalent in LINQ.

Execution engine
----------------

The LINQ implementation in .NET converts query expressions or method chains
into an abstract representation of the query in the form of expression trees.
This allows decoupling of query specification from the form of the which will
be queried. This allows queries to be applied to diverse data sources including
object sequences as represented by IEnumerable (LINQ-to-objects), database
(LINQ-to-SQL), XML (LINQ-to-XML) or indeed any other data source for which a
LINQ provider has been created.

At this stage in it`s development ``asq`` sets out to be a solid, Pythonic,
functional equivalent of LINQ-to-objects only.  With only one data provider
there is not advantage to representing queries in some abstract intermediate
representation.  An expression tree based implementation of ``asq`` may be
created in future.

Pythonic behaviour
------------------

Container creation
~~~~~~~~~~~~~~~~~~

Included in ``asq`` are several additions to support idiomatic Python usage.
The first group are the ``to_*()`` methods where * is a placeholder for various
built-in types (``list``, ``set``, ``dict``, ``tuple``) and ``asq`` provided
types (``lookup``).

Special methods
~~~~~~~~~~~~~~~

The following Python special methods are supported by the ``Queryable`` type
to support idiomatic Python usage.

  ================ =============================== =========================
  Special method   Purpose                         Equivalent query operator
  ================ =============================== =========================
  ``__contains__`` Support for the ``in`` operator ``contains()``
  ``__getitem__``  Support for indexing with []    ``element_at()``
  ``__reversed__`` Support for reversed() built-in ``reverse()``
  ``__repr__``     Stringified representation
  ``__str__``      Stringified representation      `
  ================ =============================== =========================

So, for example, the expression::

  5 in query(numbers).select(lambda: x * 2)

is equivalent to::

  query(numbers).select(lambda: x * 2).contains(5)


