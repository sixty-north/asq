``asq`` Introduction
====================

``asq`` implements a chained declarative style queries for Python *iterables*.
This provides an alternative to traditional ``for`` loops or comprehensions
which are ubiquitious in Python.  Query methods can offer the following
advantages over loops or comprehensions:

 1. **Concision**: ``asq`` query expressions can be to the point, especially
    when combining multiple queries.

 2. **Readability**: Chained ``asq`` query operators can have superior
    readability to nested or chained comprehensions.  For example, multi-key
    sorting is much clearer with ``asq`` than with other approaches.

 3. **Abstraction**: Query expressions in ``asq`` decouple query specification
    from the execution mechanism giving more flexibility with how query results
    are determined, so for example queries can be executed in parallel with
    minimal changes.

More complex queries tend to show greater benefits when using ``asq``.  Simple
transformations are probably best left as regular Python comprehensions.  It's
easy to mix and match ``asq`` with comprehensions and indeed any other Python
function which produces or consumes *iterables*.

Installing ``asq``
==================

TODO

Diving in
=========

A few simple examples will help to illustrate use of ``asq``. We'll need some
data to work with, so let's set up a simple list of student records, where each
student is represented by a dictionary::

  students = [dict(firstname='Joe', lastname='Blogs', scores=[56, 23, 21, 89]),
              dict(firstname='John', lastname='Doe', scores=[34, 12, 92, 93]),
              dict(firstname='Jane', lastname='Doe', scores=[33, 94, 91, 13]),
              dict(firstname='Ola', lastname='Nordmann', scores=[98, 23, 98, 87]),
              dict(firstname='Kari', lastname='Nordmann', scores=[86, 37, 88, 87]),
              dict(firstname='Mario', lastname='Rossi', scores=[37, 95, 45, 18])]

To avoid having to type in this data structure, you can navigate to the root of
the unpacked source distribution of asq and then import it from the
examples directory with::

  >>> from asq.examples.students import students

Now we can import the query tools we need. For our purposes the easiest thing
is to import everything from the package in one go (although remember that this
is rightly considered bad practice in programs)::

  >>> from asq.initiators import query

Let's start by creating a simple query to find those students who's first names
begin with a letter 'J'::

  >>> query(students).where(lambda student: student['firstname'].startswith('J'))
  Queryable(<filter object at 0x00000000031D9B70>)

To dissect this line and its result left to right, we have:

  1. A call to the ``query(students)``. Here ``query()`` is a query *initiator* - a
     factory function for creating a Queryable object from, in this case, an
     iterable. The ``query()`` function is the key entry point into the query
     system (although there are others).

  2. A method call to ``where()``. Where is one of the ``asq`` query operators
     and is in fact a method on the Queryable returned by the preceding call to
     ``query()``. The ``where()`` query operator accepts a single argument, which
     is a callable predicate (*i.e.* returning either True or False) function
     which which each element will be tested.

  3. The predicate passed to ``where()`` is defined by the expression ``lambda
     student: student['firstname'].startswith('J')`` which accepts a single
     argument ``student`` which is the element being tested. From the
     ``student`` dictionary the first name is extracted and the built-in string
     method ``startswith()`` is called on the name.

  4. The result of the call is a Queryable object. Note that no results have
     yet been produced - because the query has not yet been executed. The
     Queryable object contains all the information required to execute the
     query when results are required.

Initiators
----------

All query expressions begin with query *initiator*. Initiators are the entry
points to ``asq``. All initiators return Queryables on which any query method
can be called. We have already seen the ``query()`` initiator in use. The
full list of available query initiators is:

  ========================== ==================================================
  Initiator                  Purpose
  ========================== ==================================================
  ``query(iterable)``          Make a Queryable from any iterable
  ``integers(start, count)`` Make a Queryable sequence of consecutive integers
  ``repeat(value, count)``   Make a Queryable from a repeating value
  ``empty()``                Make a Queryable from an empty sequence
  ========================== ==================================================

When is the query evaluated?
----------------------------

In order to make the query execute we need to iterate over the Queryable or
chain additional calls to convert the result to, for example, a list.  We'll
do this by creating the query again, but this time assigning it to a name::

  >>> q = query(students).where(lambda student: student['firstname'].startswith('J'))
  >>> q
  Queryable(<filter object at 0x00000000031D9BE0>)
  >>> q.to_list()
  [{'lastname': 'Blogs', 'firstname': 'Joe', 'scores': [56, 23, 21, 89]},
   {'lastname': 'Doe', 'firstname': 'John', 'scores': [34, 12, 92, 93]},
   {'lastname': 'Doe', 'firstname': 'Jane', 'scores': [33, 94, 91, 13]}]

Most of the ``asq`` query operators like ``where()`` use so-called deferred
execution whereas others which return non-Queryable results use immediate
execution and force evaluation of any pending deferred operations.

Queries are executed when the results are realised by converting them to a
concrete type such as a list, dictionary or set, or by any of the query
operators which return a single value.

Query chaining
--------------

Most of the query operators can be composed in chains to create more complex
queries. For example, we could extract and compose the full names of the
three students resulting from the previous query with::

  >>> query(students).where(lambda s: s['firstname'].startswith('J'))      \
                   .select(lambda s: s['firstname'] + ' ' + s['lastname']) \
                   .to_list()
  ['Joe Blogs', 'John Doe', 'Jane Doe']

Note: The backslashes above are Python's line-continuation character, used here
for readability. They are not part of the syntax of the expression.

If we would like our results sorted by the students' minimum scores we can do::

 >>> query(students).where(lambda s: s['firstname'].startswith('J'))        \
                  .order_by(lambda s: min(s['scores']))                   \
                  .select(lambda s: s['firstname'] + ' ' + s['lastname']) \
                  .to_list()
 ['John Doe', 'Jane Doe', 'Joe Blogs']

Query nesting
-------------

TODO.

Selectors
---------

Many of the query operators, such as ``select()``, ``order_by`` or ``where()``
accept selector callables for one or more of their arguments.  Typically such
selectors are used to *select* or extract a value from an element of the
query sequence.  Selectors can be any Python callable and examples of commonly
used selectors are demonstrated below.  In addition, ``asq`` provides some
selector factories as a convenience for generating commonly used forms of
selectors.

Most of the selectors used in ``asq`` are unary functions, that is, they take
a single positional argument which is the value of the current element.
However, some of the query operators do require selectors which take two
arguments; these cases are noted in the API documentation.

Lambdas
~~~~~~~

Lambda is probably the most frequently used mechanism for specifying selectors.
This example squares each element::

  >>> numbers = [1, 67, 34, 23, 56, 34, 45]
  >>> query(numbers).select(lambda x: x**2).to_list()
  [1, 4489, 1156, 529, 3136, 1156, 2025]

Functions
~~~~~~~~~

Sometime the selector you want cannot be easily expressed as a lambda, or it is
already available as a function in existing code, such as the standard library.

In this example we use the built-in ``len()`` function as the selector::

  >>> words = 'The quick brown fox jumped over the lazy dog'.split()
  >>> words
  ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
  >>> query(words).select(len).to_list()
  [3, 5, 5, 3, 6, 4, 3, 4, 3]

Unbound methods
~~~~~~~~~~~~~~~

Unbound methods are obtained by referencing the method of a *class* rather than
the method of an *instance*. That is, the *self* parameter passed as the first
argument of a method has not yet been specified.  We can pass any unbound
method which takes only a single argument *including* the normally implicit
*self* as a selector.

In this example, we use an unbound method ``upper()`` of the built-in string
class::

  >>> words = ["the", "quick", "brown", "fox"]
  >>> query(words).select(str.upper).to_list()
  ['THE', 'QUICK', 'BROWN', 'FOX']

This has the effect of making the method call *on* each element in the
sequence.

Bound methods
~~~~~~~~~~~~~

Bound methods are obtained by referencing the method of an *instance* rather
than the method of a class.  That is, the instance referred to by the *self*
parameter passed as the first argument of a method has already been determined.

To illustrate, here we create a Multiplier class instances of which multiply by
a factor specified at initialization when the ``multiply`` method is called::

  >>> numbers = [1, 67, 34, 23, 56, 34, 45]
  >>>
  >>> class Multiplier(object):
  ...     def __init__(self, factor):
  ...         self.factor = factor
  ...     def multiply(self, value):
  ...         return self.factor * value
  ...
  >>> five_multiplier = Multiplier(5)
  >>> times_by_five  = five_multiplier.multiply
  >>> times_by_five
  <bound method Multiplier.multiply of <__main__.Multiplier object at 0x0000000002F251D0>>
  >>>
  >>> query(numbers).select(times_by_five).to_list()
  [5, 335, 170, 115, 280, 170, 225]

This has the effect of passing each element of the sequence in turn as an
argument to the bound method.

Selector factories
~~~~~~~~~~~~~~~~~~

Some selector patterns crop up very frequently and so ``asq`` provides some
simple and concise selector factories for these cases.  Selector factories are
themselves functions which return the actual selector function which can be
passed to the query operator.

  ============================= ===============================================
  Selector factory              Created selector function
  ============================= ===============================================
  ``k_(key)``                   ``lambda x: x[key]``
  ``a_(name)``                  ``lambda x: getattr(x, name)``
  ``m_(name, *args, **kwargs)`` ``lambda x: getattr(x, name)(*args, **kwargs)``
  ============================= ===============================================

Key selector factory
....................

For our example, we'll create a list of employees, with each employee being
represented as a Python dictionary::

  >>> employees = [dict(firstname='Joe', lastname='Bloggs', grade=3),
  ...              dict(firstname='Ola', lastname='Nordmann', grade=3),
  ...              dict(firstname='Kari', lastname='Nordmann', grade=2),
  ...              dict(firstname='Jane', lastname='Doe', grade=4),
  ...              dict(firstname='John', lastname='Doe', grade=3)]

Let's start by looking at an example without selector factories. Our query will
be to order the employees by descending grade, then by ascending last name and
finally by ascending first name::

  >>>  query(employees).order_by_descending(lambda employee: employee['grade']) \
  ...                .then_by(lambda employee: employee['lastname'])          \
  ...                .then_by(lambda employee: employee['firstname']).to_list()
  [{'grade': 4, 'lastname': 'Doe', 'firstname': 'Jane'},
   {'grade': 3, 'lastname': 'Bloggs', 'firstname': 'Joe'},
   {'grade': 3, 'lastname': 'Doe', 'firstname': 'John'},
   {'grade': 3, 'lastname': 'Nordmann', 'firstname': 'Ola'},
   {'grade': 2, 'lastname': 'Nordmann', 'firstname': 'Kari'}]

Those lambda expressions can be a bit of a mouthful, especially given Python's
less-than-concise lambda system.  We can improve by using less descriptive
names for the lambda arguments::

  >>>  query(employees).order_by_descending(lambda e: e['grade'])  \
  ...                .then_by(lambda e: e['lastname'])           \
  ...                .then_by(lambda e: e['firstname']).to_list()
  [{'grade': 4, 'lastname': 'Doe', 'firstname': 'Jane'},
   {'grade': 3, 'lastname': 'Bloggs', 'firstname': 'Joe'},
   {'grade': 3, 'lastname': 'Doe', 'firstname': 'John'},
   {'grade': 3, 'lastname': 'Nordmann', 'firstname': 'Ola'},
   {'grade': 2, 'lastname': 'Nordmann', 'firstname': 'Kari'}]

but there's still quite a lot of syntactic noise in here.  By using one of the
selector factories provided by ``asq`` we can make this example more concise.
The particular selector factory we are going to use is called `k_()` where the
`k` is a mnemonic for 'key' and the underscore is there purely to make the name
more unusual to avoid consuming a useful single letter variable name from the
importing namespace.  ``k_()`` takes a single argument which is the name of the
key to be used when indexing into the element, so the expressions::

  k_('foo')

and::

  lambda x: x['foo']

are equivalent because in fact the first expression is in fact returning the
second one. See how using ``k_()`` reducing the verbosity and apparent
complexity of the query somewhat::

  >>> from asq import k_
  >>> query(employees).order_by_descending(k_('grade'))   \
  ...               .then_by(k_('lastname'))            \
  ...               .then_by(k_('firstname')).to_list()
  [{'grade': 4, 'lastname': 'Doe', 'firstname': 'Jane'},
   {'grade': 3, 'lastname': 'Bloggs', 'firstname': 'Joe'},
   {'grade': 3, 'lastname': 'Doe', 'firstname': 'John'},
   {'grade': 3, 'lastname': 'Nordmann', 'firstname': 'Ola'},
   {'grade': 2, 'lastname': 'Nordmann', 'firstname': 'Kari'}]

TODO: Integer indices

Attribute selector factory
..........................

The attribute selector factory provided by ``asq`` is called `a_()` and it
creates a selector which retrieves a named attribute from each element.  To
illustrate its utility, we'll re-run the key selector exercise using the
attribute selector against ``Employee`` objects rather than dictionaries.
First of all, our ``Employee`` class::

  >>> class Employee(object):
  ...     def __init__(self, firstname, lastname, grade):
  ...         self.firstname = firstname
  ...         self.lastname = lastname
  ...         self.grade = grade
  ...     def __repr__(self):
  ...         return ("Employee(" + repr(self.firstname) + ", "
  ...                             + repr(self.lastname) + ", "
  ...                             + repr(self.grade) + ")")

Now the query and its result use the lambda form for the selectors::

  >>> query(employees).order_by_descending(lambda employee: employee.grade)  \
  ...               .then_by(lambda employee: employee.lastname)           \
  ...               .then_by(lambda employee: employee.firstname).to_list()
  [Employee('Jane', 'Doe', 4), Employee('Joe', 'Bloggs', 3),
   Employee('John', 'Doe', 3), Employee('Ola', 'Nordmann', 3),
   Employee('Kari', 'Nordmann', 2)]

We can make this query more concise by creating our selectors using the ``a_``
selector factory, where the `a` is a mnemonic for 'attribute'. ``a_()`` accepts
a single argument which is the name of the attribute to get from each element.
The expression::

  a_('foo')

is equivalent to::

  lambda x: x.foo

Using this construct we can shorted our query to the more concise::

  >>> query(employees).order_by_descending(a_('grade'))  \
  ...               .then_by(a_('lastname'))           \
  ...               .then_by(a_('firstname')).to_list()
  [Employee('Jane', 'Doe', 4), Employee('Joe', 'Bloggs', 3),
   Employee('John', 'Doe', 3), Employee('Ola', 'Nordmann', 3),
   Employee('Kari', 'Nordmann', 2)]

Method selector factory
.......................

The method-call selector factory provided by ``asq`` is called `m_()` and it
creates a selector which makes a method call on each element, optionally
passing positional or named arguments to the method. We'll re-run the attribute
selector exercise using the method selector against a modified ``Employee``
class which incorporates a couple of methods::

  >>> class Employee(object):
  ...     def __init__(self, firstname, lastname, grade):
  ...         self.firstname = firstname
  ...         self.lastname = lastname
  ...         self.grade = grade
  ...     def __repr__(self):
  ...         return ("Employee(" + repr(self.firstname)
  ...                             + repr(self.lastname)
  ...                             + repr(self.grade) + ")")
  ...     def full_name(self):
  ...         return self.firstname + " " + self.lastname
  ...     def award_bonus(self, base_amount):
  ...         return self.grade * base_amount

In its simplest form, the ``m_()`` selector factory takes a single argument,
which is the name of the method to be called as a string. So::

  m_('foo')

is equivalent to::

  lambda x: x.foo()

We can use this to easy generate a list of full names for our employees::

  >>> query(employees).select(m_('full_name')).to_list()
  ['Joe Bloggs', 'Ola Nordmann', 'Kari Nordmann', 'Jane Doe', 'John Doe']

The ``m_()`` selector factory also accepts arbitrary number of additional
positional or named arguments which will be forwarded to the method when it is
called on each element. So::

  m_('foo', 42)

is equivalent to::

  lambda x: x.foo(42)

For example to determine total cost of awarding bonuses to our employees on the
basis of grade, we can do::

  >>> query(employees).select(m_('award_bonus', 1000)).to_list()
  [3000, 3000, 2000, 4000, 3000]


Default selectors and the identity selector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any of the selector arguments to query operators in ``asq`` may be omitted [#]_
to allow the use of operators to be simplified.  When a selector is omitted
the default is used and the documentation makes it clear how that default
behaves.  In most cases, the default selector is the ``identity()`` selector.
The identity selector is very simple and is equivalent to::

  def identity(x):
      return x

That is, it is a function that returns it's only argument - essentially it's a
do-nothing function.  This is useful because frequently we don't want to select
an attribute or key from an element - we want to use the element value
directly.  For example, to sort a list of words alphabetically, we can omit the
selector passed to ``order_by()`` allowing if to default to the identity
selector::

 >>> words = "the quick brown fox jumped over the lazy dog".split()
 >>> query(words).order_by().to_list()
 ['brown', 'dog', 'fox', 'jumped', 'lazy', 'over', 'quick', 'the', 'the']

Some query operators, notably ``select()`` perform important optimisations when
used with the identity operator.  For example the operator ``select(identity)``
does nothing and simply returns the Queryable on which it was invoked.

Predicates
----------

Many of the query operators, such as ``where()``, ``distinct()``, ``skip()``,
accept predicates.  Predicates are functions which return ``True`` or
``False``.  As with selectors (see above) predicates can be defined with
lambdas, functions, unbound methods, bound methods or indeed any other callable
that returns True or False.  For convenience ``asq`` also provides some
predicate factories and combinators to concisely build predicates for common
situations.

Lambdas
~~~~~~~

  >>> numbers = [0, 56, 23, 78, 94, 56, 12, 34, 36, 90, 23, 76, 4, 67]
  >>> query(numbers).where(lambda x: x > 35).to_list()
  [56, 78, 94, 56, 36, 90, 76, 67]

Functions
~~~~~~~~~

Here we use the ``bool()`` built-in function to remove zeros from the list::

  >>> numbers = [0, 56, 23, 78, 94, 56, 12, 34, 36, 90, 23, 76, 4, 67]
  >>> query(numbers).where(bool).to_list()
  [56, 23, 78, 94, 56, 12, 34, 36, 90, 23, 76, 4, 67]

Unbound methods
~~~~~~~~~~~~~~~

  >>> a = ['zero', 'one', '2', '3', 'four', 'five', '6', 'seven', 'eight', '9']
  >>> query(a).where(str.isalpha).to_list()
  ['zero', 'one', 'four', 'five', 'seven', 'eight']

Bound methods
~~~~~~~~~~~~~

TODO ???


Predicate factories
~~~~~~~~~~~~~~~~~~~

For complex predicates inline lambdas can become quite verbose and have
limited readability.  To mitigate this somewhat, ``asq`` provides some
predicate factories and predicate combinators.

The provided predicates are:

  ============================= ===============================================
  Predicate factory             Created selector function
  ============================= ===============================================
  ``eq_(value)``                ``lambda x: x == value``
  ``ne_(value)``                ``lambda x: x != value``
  ``lt_(value)``                ``lambda x: x < value``
  ``le_(value)``                ``lambda x: x <= value``
  ``ge_(value)``                ``lambda x: x >= value``
  ``gt_(value)``                ``lambda x: x >= value``
  ``is_(value)``                ``lambda x: x is value``
  ``contains_(value)``          ``lambda x: value in x``
  ============================= ===============================================

Predicates are available in the ``predicates`` module of the ``asq`` package::

  >>> from asq.predicates import *

So given::

  >>> numbers = [0, 56, 23, 78, 94, 56, 12, 34, 36, 90, 23, 76, 4, 67]

the query expression::

  >>> query(numbers).where(lambda x: x > 35).take_while(lambda x: x < 90).to_list()
  [56, 78]

could be written more concisely as::

  >>> query(numbers).where(gt_(35)).take_while(lt_(90)).to_list()
  [56, 78]


Predicate combinator factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some simple combinators are provided to allow the predicate factories to be
combined to form more powerful expressions. These combinators are,

  ============================= ===============================================
  Combinator factory             Created selector function
  ============================= ===============================================
  ``not_(a)``                   ``lambda x: not a(x)``
  ``and_(a, b)``                ``lambda x: a(x) and b(x)``
  ``or_(a, b)``                 ``lambda x: a(x) or b(x)``
  ``xor(a, b)``                 ``lambda x: a(x) != b(x)``
  ============================= ===============================================

where ``a`` and ``b`` are themselves predicates.

So given::

  >>> numbers = [0, 56, 23, 78, 94, 56, 12, 34, 36, 90, 23, 76, 4, 67]

the query expression::

  >>> query(numbers).where(lambda x: x > 20 and x < 80).to_list()
  [56, 23, 78, 56, 34, 36, 23, 76, 67]


could be expressed as::

  >>> query(numbers).where(and_(gt_(20), lt_(80).to_list()
  [56, 23, 78, 56, 34, 36, 23, 76, 67]


Although complex expressions are probably still better expressed as lambdas or
separate functions altogether.

Using selector factories for predicates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A predicate is any callable that returns ``True`` or ``False``, so any selector
which returns ``True`` or ``False`` is by definition a predicate. This means
that the selector factories ``k_()``, ``a_()`` and ``m_()`` may also be used as
predicate factories so long as they return boolean values. They may also be
used with the predicate combinators.  For example, consider a sequence of
``Employee`` objects which have an ``intern`` attribute which evaluates to True
or False.  We can filter out interns using this query::

  >>> query(employees).where(not_(a_('intern')))


Comparers
---------

TODO: Document comparers


Debugging
---------

With potentially so much deferred execution occuring, debugging ``asq`` query
expressions using tools such as debuggers can be challenging. Furthermore, since
queries are expressions use of statements such as Python 2 ``print`` can be
awkward.

To ease debugging, ``asq`` provides a logging facility which can be used to
display intermediate results with an optional abiliity for force full, rather
than lazy, evaluation of sequences.

To demonstrate, let's start with a bug-ridden implementation of Fizz-Buzz
implemented with ``asq``. Fizz-Buzz is a game where the numbers 1 to 100 are
read aloud but for numbers divisible by three "Fizz" is shouted, and for numbers
divisible by five, "Buzz" is shouted.

  >>> from asq.initiators import integers
  >>> integers(1, 100).select(lambda x: "Fizz" if x % 3 == 0 else x) \
  ...                 .select(lambda x: "Buzz" if x % 5 == 0 else x).to_list()

At a glance this looks like it should work, but when run we get::

  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "asq/queryables.py", line 1910, in to_list
      lst = list(self)
    File "<stdin>", line 1, in <lambda>
  TypeError: not all arguments converted during string formatting

To investigate further it would be useful to examine the intermediate results.
We can do this using the ``log()`` query operator, which accepts any logger
supporting a ``debug(message)`` method. We can get just such a logger from the
Python standard library ``logging`` module::

  >>> import logging
  >>> clog = logging.getLogger("clog")
  >>> clog.setLevel(logging.DEBUG)

which creates a console logger we have called ``clog``::

  >>> from asq.initiators import integers
  >>> integers(1, 100) \
  ...  .select(lambda x: "Fizz" if x % 3 == 0 else x).log(clog, label="Fizz select"). \
  ...  .select(lambda x: "Buzz" if x % 5 == 0 else x).to_list()
  DEBUG:clog:Fizz select : BEGIN (DEFERRED)
  DEBUG:clog:Fizz select : [0] yields 1
  DEBUG:clog:Fizz select : [1] yields 2
  DEBUG:clog:Fizz select : [2] yields 'Fizz'
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "asq/queryables.py", line 1910, in to_list
      lst = list(self)
    File "<stdin>", line 1, in <lambda>
  TypeError: not all arguments converted during string formatting

so we can see the the first select operator yields 1, 2, 'Fizz' before the
failure. Now it's perhaps more obvious that when x in the second lambda is equal
to 'Fizz' the ``%`` operator will be operating on a string on its left-hand side
and so the ```%`` will perform string interpolation rather than modulus. This is
the cause of the error we see.

We can fix this by not applying the modulus operator in the case that x is
'Fizz'::

  >>> integers(1, 100).select(lambda x: "Fizz" if x % 3 == 0 else x).log(clog, label="Fizz select") \
                      .select(lambda x: "Buzz" if x != "Fizz" and x % 5 == 0 else x).to_list()
  DEBUG:clog:Fizz select : BEGIN (DEFERRED)
  DEBUG:clog:Fizz select : [0] yields 1
  DEBUG:clog:Fizz select : [1] yields 2
  DEBUG:clog:Fizz select : [2] yields 'Fizz'
  DEBUG:clog:Fizz select : [3] yields 4
  DEBUG:clog:Fizz select : [4] yields 5
  DEBUG:clog:Fizz select : [5] yields 'Fizz'
  DEBUG:clog:Fizz select : [6] yields 7
  DEBUG:clog:Fizz select : [7] yields 8
  DEBUG:clog:Fizz select : [8] yields 'Fizz'
  DEBUG:clog:Fizz select : [9] yields 10
  DEBUG:clog:Fizz select : [10] yields 11
  DEBUG:clog:Fizz select : [11] yields 'Fizz'
  DEBUG:clog:Fizz select : [12] yields 13
  DEBUG:clog:Fizz select : [13] yields 14
  DEBUG:clog:Fizz select : [14] yields 'Fizz'
  DEBUG:clog:Fizz select : [15] yields 16
  DEBUG:clog:Fizz select : [16] yields 17
  ...
  DEBUG:clog2:Fizz select : [98] yields 'Fizz'
  DEBUG:clog2:Fizz select : [99] yields 100
  DEBUG:clog2:Fizz select : END (DEFERRED)
  [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14,
   'Fizz', 16, 17, 'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26,
   'Fizz', 28, 29, 'Fizz', 31, 32, 'Fizz', 34, 'Buzz', 'Fizz', 37, 38, 'Fizz',
   'Buzz', 41, 'Fizz', 43, 44, 'Fizz', 46, 47, 'Fizz', 49, 'Buzz', 'Fizz', 52,
   53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'Fizz', 61, 62, 'Fizz', 64, 'Buzz',
   'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'Fizz', 76, 77, 'Fizz',
   79, 'Buzz', 'Fizz', 82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'Fizz', 91,
   92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz', 'Buzz']

The problem is solved, but inspection of the output shows that our query
expression produces incorrect results for those numbers which are multiples of
both 3 and 5, such as 15, for which we should be returning 'FizzBuzz'. For the
sake of completeness, let's modify the expression to deal with this::

  >>> integers(1, 100).select(lambda x: "FizzBuzz" if x % 15 == 0 else x) \
                      .select(lambda x: "Fizz" if x != "FizzBuzz" and x % 3 == 0 else x) \
                      .select(lambda x: "Buzz" if x != "FizzBuzz" and x != "Fizz" and x % 5 == 0 else x).to_list()
  [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14,
   'FizzBuzz', 16, 17, 'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26,
   'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34, 'Buzz', 'Fizz', 37, 38,
   'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz',
   'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62,
   'Fizz', 64, 'Buzz', 'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74,
   'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83, 'Fizz', 'Buzz', 86,
   'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98,
   'Fizz', 'Buzz']

Extending ``asq``
-----------------

TODO: Document extending asq


.. [#] Except the single selector argument to the ``select()`` operator itself.