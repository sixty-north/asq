API Reference
*************

.. contents:: Table of Contents
   :depth: 2

Generators
==========

Selectors
=========

Queryables
==========

.. automodule:: asq.queryable

Queryable
---------

   .. autoclass:: Queryable

      .. autosummary::
         :nosignatures:

         .. currentmodule asq.queryable

         Queryable.__contains__
         Queryable.__enter__
         Queryable.__exit__
         Queryable.__getitem__
         Queryable.__init__
         Queryable.__iter__
         Queryable.__reversed__
         Queryable.__repr__
         Queryable.__str__
         Queryable.aggregate
         Queryable.all
         Queryable.any
         Queryable.as_parallel
         Queryable.average
         Queryable.close
         Queryable.closed
         Queryable.concat
         Queryable.contains
         Queryable.count
         Queryable.default_if_empty
         Queryable.difference
         Queryable.distinct
         Queryable.element_at
         Queryable.first
         Queryable.first_or_default
         Queryable.group_by
         Queryable.group_join
         Queryable.intersect
         Queryable.join
         Queryable.last
         Queryable.last_or_default
         Queryable.log
         Queryable.max
         Queryable.min
         Queryable.of_type
         Queryable.order_by
         Queryable.order_by_descending
         Queryable.select
         Queryable.select_many
         Queryable.select_many_with_correspondence
         Queryable.select_many_with_index
         Queryable.select_with_index
         Queryable.sequence_equal
         Queryable.single
         Queryable.single_or_default
         Queryable.skip
         Queryable.skip_while
         Queryable.sum
         Queryable.take
         Queryable.take_while
         Queryable.to_dictionary
         Queryable.to_list
         Queryable.to_lookup
         Queryable.to_set
         Queryable.to_str
         Queryable.to_tuple
         Queryable.union
         Queryable.where
         Queryable.zip

      .. automethod:: __contains__(item)

         .. note::

            A chainable query operator called ``contains()`` (no underscores)
            is also provided.

         .. rubric:: Example

         Test whether 49 is one of the squares of two, seven or nine::

           >>> a = [2, 7, 9]
           >>> 49 in asq(a).select(lambda x: x*x)
           True
           
      .. automethod:: __enter__()

      .. automethod:: __exit__(type, value, traceback)

      .. automethod:: __getitem__(index)

         .. note::

            A chainable query operator called ``element_at()`` is also
            provided.

         .. rubric:: Examples

         Retrieve the fourth element of a greater than six::

           >>> a = [7, 3, 9, 2, 1, 10, 11, 4, 13]
           >>> asq(a).where(lambda x: x > 6)[3]
           11

      .. automethod:: __init__(iterable)

         .. rubric:: Example

         Initialise a queryable from a list::

           >>> a = [1, 5, 7, 8]
           >>> queryable = Queryable(a)

         .. note::

            The ``asq(iterable)`` initiator should normally be used in
            preference to calling the ``Queryable`` constructor directly.

      .. automethod:: __iter__()

        .. note::

           This method should not usually be called directly; use the
           ``iter()`` built-in or other Python constructs which check for the
           presence of ``__iter__()``, such as ``for`` loops::

        .. rubric:: Examples

        Call ``__iter__()`` indirectly through the ``iter()`` built-in to
        obtain an iterator over the query results::

          >>> a = [8, 9, 2]
          >>> q = asq(a)
          >>> iterator = iter(q)
          >>> next(iterator)
          8
          >>> next(iterator)
          9
          >>> next(iterator)
          2
          >>> next(iterator)
          StopIteration

        Call ``__iter__()`` indirectly by using a ``for`` loop::

          >>> a = [1, 9, 4]
          >>> q = asq(a)
          >>> for v in q:
          ...     print(v)
          ...
          1
          9
          4

      .. automethod:: __reversed__()

         .. note::

            A chainable query operator called ``reverse()`` is also
            provided.

         .. note::

            This method should not usually be called directly; use the
            ``reversed()` built-in or other Python constructs which check for
            the presence of __reversed__().

         .. rubric:: Example

         Create a reverse iterator over a queryable for use with a ``for``
         loop::

           >>> a = [7, 3, 9, 2, 1]
           >>> q = asq(a)
           >>> for v in reversed(q):
           ...     print(v)
           ...
           1
           2
           9
           3
           7

      .. automethod:: __repr__()

         .. note::

            This method should not usually be called directly; use the
            ``str()`` built-in or other Python constructs which check for the
            presence of __str__ such as string interpolation functions.

         Provide a string representation of the  Queryable using the ``repr()``
         built-in::

           >>> a = [9, 7, 8]
           >>> q = asq(a)
           >>> str(q)
           'Queryable([9, 7, 8])'

      .. automethod:: __str__()

         .. note::

            This method should not usually be called directly; use the
            ``str()`` built-in or other Python constructs which check for the
            presence of __str__ such as string interpolation functions.

         .. note::

            In order to convert the Queryable sequence to a string based on the
            element values, consider using the ``to_str()`` method.

         .. rubric:: Example

         Convert the Queryable to a string using the ``str()`` built-in::

           >>> a = [9, 7, 8]
           >>> q = asq(a)
           >>> str(q)
           'Queryable([9, 7, 8])'

      .. automethod:: aggregate(reducer, seed=sentinel, result_selector=identity)

         .. rubric:: Examples

         Compute the product of a list of numbers::

           >>> numbers = [4, 7, 3, 2, 1, 9]
           >>> asq(numbers).aggregate(lambda accumulator, update: accumulator * update)
           1512

         Concatenate strings to an initial seed value::

           >>> cheeses = ['Cheddar', 'Stilton', 'Cheshire', 'Beaufort', 'Brie']
           >>> asq(cheeses).aggregate(lambda a, u: a + ' ' + u, seed="Cheeses:")
           'Cheeses: Cheddar Stilton Cheshire Beaufort Brie'

         Concatenate text fragments using ``operator.add()`` and return the
         number of words::

           >>> from operator import add
           >>> fragments = ['The quick ', 'brown ', 'fox jumped over ', 'the ', 'lazy dog.']
           >>> asq(fragments).aggregate(add, lambda result: len(result.split()))
           9

      .. automethod:: all(predicate=bool)

         .. rubric:: Examples

         Determine whether all values evaluate to True in a boolean context::

           >>> items = [5, 2, "camel", 3.142, (3, 4, 9)]
           >>> asq(objects).all()
           True

         Check that all numbers are divisible by 13::
         
           >>> numbers = [260, 273, 286, 299, 312, 325, 338, 351, 364, 377]
           >>> asq(numbers).all(lambda x: x % 13 == 0)
           True

      .. automethod:: any(predicate=None)

         .. rubric:: Examples

         Determine whether the sequence contains any items::

           >>> items = [0, 0, 0]
           >>> asq(items).any()
           True

         Determine whether the sequence contains any items which are a multiple
         of 13::

           >>> numbers = [98, 458, 32, 876, 12, 9, 325]
           >>> asq(numbers).any(lambda x: x % 13 == 0)
           True

      .. automethod:: as_parallel(pool=None)

      .. automethod:: average(selector=identity)

         .. rubric:: Examples

         Compute the average of some numbers::

           >>> numbers = [98, 458, 32, 876, 12, 9, 325]
           >>> asq(numbers).average()
           258.57142857142856

         Compute the mean square of a sequence::

           >>> numbers = [98, 458, 32, 876, 12, 9, 325]
           >>> asq(numbers).average(lambda x: x*x)
           156231.14285714287

      .. automethod:: close()

      .. automethod:: closed()

      .. automethod:: concat(second_iterable)

         .. rubric:: Example

         Concatenate two sequences of numbers:

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).concat([98, 23, 23, 12]).to_list()
           [1, 45, 23, 34, 98, 23, 23, 12]

      .. automethod:: contains(value, equality_comparer=operator.eq)

         .. rubric:: Example

         Check whether a sentence contains a particular word::

           >>> words = ['A', 'man', 'a', 'plan', 'a', 'canal', 'Panama']
           >>> words.contains('plan')
           True

         Check whether a sentence contains a particular word with a case-
         insensitive check::

           >>> words = ['A', 'man', 'a', 'plan', 'a', 'canal', 'Panama']
           >>> asq(words).contains('panama',
           ...                     lambda lhs, rhs: lhs.lower() == rhs.lower())
           True
           
      .. automethod:: count(predicate=None)

         .. rubric:: Examples

         Count the number of elements in a sequence::

           >>> people = ['Sheila', 'Jim', 'Fred']
           >>> asq(people).count()
           3

         Count the number of names containing the letter 'i'::

           >>> people = ['Sheila', 'Jim', 'Fred']
           >>> asq(people).count(lambda s: 'i' in s)
           3 

      .. automethod:: default_if_empty(default)

         .. rubric:: Examples

         An empty sequence triggering the default return::

           >>> e = []
           >>> asq(e).default_if_empty(97).to_list()
           [97]

         A non-empty sequence passing through::

           >>> f = [70, 45, 34]
           >>> asq(f).default_if_empty(97).to_list()
           [70, 45, 34]

      .. automethod:: difference(second_iterable, selector=identity)

         .. rubric:: Examples

         Numbers in the first list which are not in the second list::

           >>> a = [0, 2, 4, 5, 6, 8, 9]
           >>> b = [1, 3, 5, 7, 8]
           >>> asq(a).difference(b).to_list()
           [0, 2, 4, 6, 9]

         Countries in the first list which are not in the second list, compared
         in a case-insensitive manner::

           >>> a = ['UK', 'Canada', 'qatar', 'china', 'New Zealand', 'Iceland']
           >>> b = ['iceland', 'CANADA', 'uk']
           >>> asq(a).difference(b, lambda x: x.lower()).to_list()
           ['qatar', 'china', 'New Zealand']

      .. automethod:: distinct(selector=identity)

         .. rubric:: Examples

         Remove duplicate numbers::

           >>> d = [0, 2, 4, 5, 6, 8, 9, 1, 3, 5, 7, 8]
           >>> asq(d).distinct().to_list()
           [0, 2, 4, 5, 6, 8, 9, 1, 3, 7]

         A sequence such that no two numbers in the result have digits which
         sum to the same value::

           >>> e = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> def sum_of_digits(num):
           ...     return sum(int(i) for i in str(num))
           ...
           >>> asq(e).distinct(sum_of_digits).to_list()
           [10, 34, 56, 11, 89]

      .. automethod:: element_at(index)

         .. rubric:: Example

         Retrieve the fifth element from a list::

           >>> f = [10, 34, 56, 11, 89]
           >>> asq(f).element_at(4)
           89

      .. automethod:: first(predicate=None)

         .. rubric:: Examples

         Retrieve the first element of a sequence::

           >>> e = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> asq(e).first()
           10

         Retrieve the first element of a sequence divisible by seven::

           >>> e = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> asq(e).first(lambda x: x % 7 == 0)
           56

      .. automethod:: first_or_default(default, predicate=None)

         .. rubric:: Examples

         Retrieve the first element of a sequence::

           >>> e = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> asq(e).first_or_default(14)
           10

         Return the default when called on an empty sequence::

           >>> f = []
           >>> asq(f).first_or_default(17)
           17

         Retrieve the first element of a sequence divisible by eight::

           >>> e = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> asq(e).first_or_default(10, lambda x: x % 8 == 0)
           56

      .. automethod:: group_by(key_selector=identity, element_selector=identity, result_selector=lambda key, grouping: grouping)

         .. rubric:: Examples

         Group numbers by the remainder when dividing them by five::

           >>> numbers = [10, 34, 56, 43, 74, 25, 11, 89]
           >>> groups = asq(e).group_by(lambda x: x % 5).to_list()
           >>> groups
           [Grouping(key=0), Grouping(key=4), Grouping(key=1),
            Grouping(key=3)]
           >>> groups[0].key
           0
           >>> groups[0].to_list()
           [10, 25]
           >>> groups[1].key
           1
           >>> groups[1].to_list()
           [34, 74, 89]

         Group people by their nationality of the first name, and place only
         the person's name in the grouped result::

           >>> people = [ dict(name="Joe Bloggs", nationality="British"),
           ...            dict(name="Ola Nordmann", nationality="Norwegian"),
           ...            dict(name="Harry Holland", nationality="Dutch"),
           ...            dict(name="Kari Nordmann", nationality="Norwegian"),
           ...            dict(name="Jan Kowalski", nationality="Polish"),
           ...            dict(name="Hans Schweizer", nationality="Swiss"),
           ...            dict(name="Tom Cobbleigh", nationality="British"),
           ...            dict(name="Tommy Atkins", nationality="British") ]
           >>> groups = asq(people).group_by(lambda p: p['nationality'],
                                             lambda p: p['name']).to_list()
           >>> groups
           [Grouping(key='British'), Grouping(key='Norwegian'),
            Grouping(key='Dutch'), Grouping(key='Polish'),
            Grouping(key='Swiss')]
           >>> groups[0].to_list()
           ['Joe Bloggs', 'Tom Cobbleigh', 'Tommy Atkins']
           >>> groups[1].to_list()
           ['Ola Nordmann', 'Kari Nordmann']

         Determine the number of people in each national group by creating
         a tuple for each group where the first element is the nationality and
         the second element is the number of people of that nationality::

           >>> people = [ dict(name="Joe Bloggs", nationality="British"),
           ...            dict(name="Ola Nordmann", nationality="Norwegian"),
           ...            dict(name="Harry Holland", nationality="Dutch"),
           ...            dict(name="Kari Nordmann", nationality="Norwegian"),
           ...            dict(name="Jan Kowalski", nationality="Polish"),
           ...            dict(name="Hans Schweizer", nationality="Swiss"),
           ...            dict(name="Tom Cobbleigh", nationality="British"),
           ...            dict(name="Tommy Atkins", nationality="British") ]
           >>> groups = asq(people).group_by(lambda p: p['nationality'],
           ...  result_selector=lambda key, group: (key, len(group))).to_list()
           >>> groups
           [('British', 3), ('Norwegian', 2), ('Dutch', 1), ('Polish', 1),
            ('Swiss', 1)]
           
      .. automethod:: group_join(inner_iterable, outer_key_selector=identity, inner_key_selector=identity, result_selector=lambda outer, grouping: grouping)

         .. rubric:: Example

         Correlate players with soccer teams using the team name. Group
         the players within those teams such that each element of the
         result sequence contains full information about a team and a
         collection of players belonging to that team::

           >>> players = [dict(name="Ferdinand", team="Manchester United"),
           ...            dict(name="Cole", team="Chelsea", fee=5),
           ...            dict(name="Crouch", team="Tottenham Hotspur"),
           ...            dict(name="Downing", team="Aston Villa"),
           ...            dict(name="Lampard", team="Chelsea", fee=11),
           ...            dict(name="Rooney", team="Manchester United"),
           ...            dict(name="Scholes", team="Manchester United", fee=None)]
           >>> teams = [dict(name="Manchester United", ground="Old Trafford"),
           ...          dict(name="Chelsea", ground="Stamford Bridge"),
           ...          dict(name="Tottenham Hotspur", ground="White Hart Lane"),
           ...          dict(name="Aston Villa", ground="Villa Park")]
           >>> q = asq(teams).group_join(players, lambda team: team['name'],
           ...               lambda player: player['team'],
           ...               lambda team, grouping: dict(team=team['name'],
           ...                                           ground=team['ground'],
           ...                                           players=grouping)).to_list()
           >>> q
           [{'players': Grouping(key='Manchester United'), 'ground': 'Old Trafford', 'team': 'Manchester United'},
            {'players': Grouping(key='Chelsea'), 'ground': 'Stamford Bridge', 'team': 'Chelsea'},
            {'players': Grouping(key='Tottenham Hotspur'), 'ground': 'White Hart Lane', 'team': 'Tottenham Hotspur'},
            {'players': Grouping(key='Aston Villa'), 'ground': 'Villa Park', 'team': 'Aston Villa'}]
           >>> q[0]['players'].to_list()
           [{'name': 'Ferdinand', 'team': 'Manchester United'},
            {'name': 'Rooney', 'team': 'Manchester United'},
            {'name': 'Scholes', 'team': 'Manchester United'}]

      .. automethod:: intersect(second_iterable, selector=identity)

         .. rubric:: Examples

         Find all the numbers common to both lists ``a`` and ``b``::

           >>> a = [1, 6, 4, 2, 6, 7, 3, 1]
           >>> b = [6, 2, 1, 9, 2, 5]
           >>> asq(a).intersect(b).to_list()
           [1, 6, 2]

         Take those strings from the list ``a`` which also occur in list ``b``
         when compared in a case-insensitive way::

           >>> a = ["Apple", "Pear", "Banana", "Orange", "Strawberry"]
           >>> b = ["PEAR", "ORANGE", "BANANA", "RASPBERRY", "BLUEBERRY"]
           >>> asq(a).intersect(b, lambda s: s.lower()).to_list()
           ['Pear', 'Banana', 'Orange']

      .. automethod:: join(inner_iterable, outer_key_selector=identity, inner_key_selector=identity, result_selector=lambda outer, inner: (outer, inner))

         .. rubric:: Examples

         Correlate pets with their owners, producing pairs of pet and owner
         date for each result::

           >>> people = ['Minnie', 'Dennis', 'Roger', 'Beryl']
           >>> pets = [dict(name='Chester', owner='Minnie'),
           ...         dict(name='Gnasher', owner='Dennis'),
           ...         dict(name='Dodge', owner='Roger'),
           ...         dict(name='Pearl', owner='Beryl')]
           >>> asq(pets).join(people, lambda pet: pet['owner']).to_list()
           [({'owner': 'Minnie', 'name': 'Chester'}, 'Minnie'),
            ({'owner': 'Dennis', 'name': 'Gnasher'}, 'Dennis'),
            ({'owner': 'Roger', 'name': 'Dodge'}, 'Roger'),
            ({'owner': 'Beryl', 'name': 'Pearl'}, 'Beryl')]

         or correlate owners with pets, producing more refined results::

           >>> asq(people).join(pets, inner_key_selector=lambda pet: pet['owner'],
           ...   result_selector=lambda person, pet: pet['name'] + " is owned by " + person) \
           ...   .to_list()
           ['Chester is owned by Minnie',
            'Gnasher is owned by Dennis',
            'Dodge is owned by Roger',
            'Pearl is owned by Beryl']

      .. automethod:: last(predicate=None)

         .. rubric:: Examples

         Return the last number in this sequence::

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).last()
           34

         Return the last number under 30 in this sequence::

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).last(lambda x: x < 30)
           23

      .. automethod:: last_or_default(default, predicate=None)

         .. rubric:: Examples

         Return the last number in this sequence::

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).last()
           34

         Return the last number under 30 in this sequence::

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).last(lambda x: x < 30)
           23

         Trigger return of the default using a sequence with no values which
         satisfy the predicate::

           >>> numbers = [1, 45, 23, 34]
           >>> asq(numbers).last_or_default(100, lambda x: x > 50)
           100

         Trigger return of the default using an empty sequence::

           >>> numbers = []
           >>> asq(numbers).last_or_default(37)
           37

      .. automethod:: log(logger=None, label=None, eager=False)

         .. rubric:: Examples

         These examples log to a console logger called ``clog`` which can be
         created using the following incantation::

           >>> import logging
           >>> clog = logging.getLogger("clog")
           >>> clog.setLevel(logging.DEBUG)
           >>> clog.addHandler(logging.StreamHandler())

         By default, ``log()`` uses deferred execution, so unless the output
         of ``log()`` is consumed nothing at all will be logged. In this
         example nothing is logged to the console because the result of
         ``log()`` is never consumed::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog)

         We can easily consume the output of ``log()`` by chaining a call to
         ``to_list()``. Use the default arguments for ``log()``::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog).to_list()
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : BEGIN (DEFERRED)
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [0] yields 1
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [1] yields 5
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [2] yields 9
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [3] yields 34
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [4] yields 2
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [5] yields 9
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [6] yields 12
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [7] yields 7
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [8] yields 13
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [9] yields 48
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [10] yields 34
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [11] yields 23
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [12] yields 34
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [13] yields 9
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : [14] yields 47
           Queryable([1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]) : END (DEFERRED)
           [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]

         The beginning and end of the sequence are delimited by ``BEGIN`` and
         ``END`` markers which also indicated whether logging is ``DEFERRED``
         so items are logged only as they are requested or ``EAGER`` where the
         whole sequence will be returns immediately.

         From left to right the log output shows:

           1. A label, which defaults to the ``repr()`` of the Queryable
              instance being logged.

           2. In square brackets the zero-based index of the element being
              logged.

           3. ``yields <element>`` showing the element value

         Specify a label a more concise label to ``log()``::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog, label='asq()').to_list()
           asq() : BEGIN (DEFERRED)
           asq() : [0] yields 1
           asq() : [1] yields 5
           asq() : [2] yields 9
           asq() : [3] yields 34
           asq() : [4] yields 2
           asq() : [5] yields 9
           asq() : [6] yields 12
           asq() : [7] yields 7
           asq() : [8] yields 13
           asq() : [9] yields 48
           asq() : [10] yields 34
           asq() : [11] yields 23
           asq() : [12] yields 34
           asq() : [13] yields 9
           asq() : [14] yields 47
           asq() : END (DEFERRED)
           [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]

         We can show how the default deferred logging produces only required
         elements by only consuming the first three elements::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog, label='asq()').take(3).to_list()
           asq() : BEGIN (DEFERRED)
           asq() : [0] yields 1
           asq() : [1] yields 5
           asq() : [2] yields 9
           [1, 5, 9]

         However, by setting the ``eager`` argument to be True, we can force
         logging of the whole sequence immediately::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog, label='asq()', eager=True).take(3).to_list()
           asq() : BEGIN (EAGER)
           asq() : [0] = 1
           asq() : [1] = 5
           asq() : [2] = 9
           asq() : [3] = 34
           asq() : [4] = 2
           asq() : [5] = 9
           asq() : [6] = 12
           asq() : [7] = 7
           asq() : [8] = 13
           asq() : [9] = 48
           asq() : [10] = 34
           asq() : [11] = 23
           asq() : [12] = 34
           asq() : [13] = 9
           asq() : [14] = 47
           asq() : END (EAGER)
           [1, 5, 9]

         Note that in these cases the output has a different format and that
         use of eager logging in no way affects the query result.

         If ``logger`` is None (or omitted), then logging is disabled
         completely::

           >>> asq(numbers).log(logger=None, label='asq()').take(3).to_list()
           [1, 5, 9]

         Finally, see that ``log()`` can be used at multiple points within a
         query expression::

           >>> numbers = [1, 5, 9, 34, 2, 9, 12, 7, 13, 48, 34, 23, 34, 9, 47]
           >>> asq(numbers).log(clog, label='asq(numbers)')                   \
           ...        .select(lambda x: x * x).log(clog, label='squared')     \
           ...        .where(lambda x: x > 1000).log(clog, label="over 1000") \
           ...        .take(3).log(clog, label="take 3")                      \
           ...        .to_list()
           take 3 : BEGIN (DEFERRED)
           over 1000 : BEGIN (DEFERRED)
           squared : BEGIN (DEFERRED)
           asq(numbers) : BEGIN (DEFERRED)
           asq(numbers) : [0] yields 1
           squared : [0] yields 1
           asq(numbers) : [1] yields 5
           squared : [1] yields 25
           asq(numbers) : [2] yields 9
           squared : [2] yields 81
           asq(numbers) : [3] yields 34
           squared : [3] yields 1156
           over 1000 : [0] yields 1156
           take 3 : [0] yields 1156
           asq(numbers) : [4] yields 2
           squared : [4] yields 4
           asq(numbers) : [5] yields 9
           squared : [5] yields 81
           asq(numbers) : [6] yields 12
           squared : [6] yields 144
           asq(numbers) : [7] yields 7
           squared : [7] yields 49
           asq(numbers) : [8] yields 13
           squared : [8] yields 169
           asq(numbers) : [9] yields 48
           squared : [9] yields 2304
           over 1000 : [1] yields 2304
           take 3 : [1] yields 2304
           asq(numbers) : [10] yields 34
           squared : [10] yields 1156
           over 1000 : [2] yields 1156
           take 3 : [2] yields 1156
           take 3 : END (DEFERRED)
           [1156, 2304, 1156]
           
      .. automethod:: max(selector=identity)

         .. rubric:: Examples

         Return the maximum value from a list of numbers::

           >>> numbers = [1, -45, 23, -34, 19]
           >>> asq(numbers).max()
           23

         Return the maximum absolute value from a list of numbers::

           >>> numbers = [1, -45, 23, -34, 19]
           >>> asq(numbers).max(abs)
           45

      .. automethod:: min(selector=identity)

        .. rubric:: Examples

        Return the minimum value from a list of numbers::

           >>> numbers = [1, -45, 23, -34, 19]
           >>> asq(numbers).max()
           -45

        Return the minimum absolute value from a list of numbers::

           >>> numbers = [1, -45, 23, -34, 19]
           >>> asq(numbers).max(abs)
           1

      .. automethod:: of_type(classinfo)

         .. rubric:: Examples

         Return all of the strings from a list::

           >>> numbers = ["one", 2.0, "three", "four", 5, 6.0, "seven", 8, "nine", "ten"]
           >>> asq(numbers).of_type(int).to_list()
           [5, 8]

         Return all the integers and floats from a list::

           >>> numbers = ["one", 2.0, "three", "four", 5, 6.0, "seven", 8, "nine", "ten"]
           >>> asq(numbers).of_type((int, float)).to_list()
           [2.0, 5, 6.0, 8]

      .. automethod:: order_by(key_selector=identity)

         .. rubric:: Examples

         Sort a list of numbers in ascending order by their own value::

           >>> numbers = [1, -45, 23, -34, 19, 78, -23, 12, 98, -14]
           >>> asq(numbers).order_by().to_list()
           [-45, -34, -23, -14, 1, 12, 19, 23, 78, 98]

         Sort a list of numbers in ascending order by their absolute value::

           >>> numbers = [1, -45, 23, -34, 19, 78, -23, 12, 98, -14]
           >>> asq(numbers).order_by(abs).to_list()
           [1, 12, -14, 19, 23, -23, -34, -45, 78, 98]

         See that the relative order of the two elements which compare equal
         (23 and -23 in the list shown) are preserved; the sort is stable.

      .. automethod:: order_by_descending(key_selector=identity)

         .. rubric:: Examples

         Sort a list of numbers in ascending order by their own value::

           >>> numbers = [1, -45, 23, -34, 19, 78, -23, 12, 98, -14]
           >>> asq(numbers).order_by_descending().to_list()
           [98, 78, 23, 19, 12, 1, -14, -23, -34, -45]

         Sort a list of numbers in ascending order by their absolute value::

           >>> numbers = [1, -45, 23, -34, 19, 78, -23, 12, 98, -14]
           >>> asq(numbers).order_by_descending(abs).to_list()
           [98, 78, -45, -34, 23, -23, 19, -14, 12, 1]

         See that the relative order of the two elements which compare equal
         (23 and -23 in the list shown) are preserved; the sort is stable.

      .. automethod:: select(selector)

         .. rubric:: Examples

         Select the scores from a collection of student records::

           >>> students = [dict(name="Joe Bloggs", score=54),
           ...             dict(name="Ola Nordmann", score=61),
           ...             dict(name="John Doe", score=51),
           ...             dict(name="Tom Cobleigh", score=71)]
           >>> asq(students).select(lambda student: student['score']).to_list()
           [54, 61, 51, 71]

         Transform a sequence of numbers into it square roots::

           >>> import math
           >>> numbers = [1, 45, 23, 34, 19, 78, 23, 12, 98, 14]
           >>> asq(numbers).select(math.sqrt).to_list()
           [1.0, 6.708203932499369, 4.795831523312719, 5.830951894845301,
            4.358898943540674, 8.831760866327848, 4.795831523312719,
            3.4641016151377544, 9.899494936611665, 3.7416573867739413]

      .. automethod:: select_many(collection_selector=identity, result_selector=identity)

         .. rubric:: Examples

         Select all the words from three sentences by splitting each sentence
         into its component words::

           >>> a = "The quick brown fox jumped over the lazy dog"
           >>> b = "Pack my box with five dozen liquor jugs"
           >>> c = "Jackdaws love my big sphinx of quartz"
           >>> sentences = [a, b, c]
           >>> asq(sentences).select_many(lambda sentence: sentence.split()).to_list()
           ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
            'dog', 'Pack', 'my', 'box', 'with', 'five', 'dozen', 'liquor',
            'jugs', 'Jackdaws', 'love', 'my', 'big', 'sphinx', 'of', 'quartz']

         Select all the words from three sentences and return a list of the
         length of each word::

           >>> a = "The quick brown fox jumped over the lazy dog"
           >>> b = "Pack my box with five dozen liquor jugs"
           >>> c = "Jackdaws love my big sphinx of quartz"
           >>> sentences = [a, b, c]
           >>> asq(sentences).select_many(lambda sentence: sentence.split(), len).to_list()
           [3, 5, 5, 3, 6, 4, 3, 4, 3, 4, 2, 3, 4, 4, 5, 6, 4, 8, 4, 2, 3, 6,
            2, 6]

      .. automethod:: select_many_with_correspondence(collection_selector=identity, result_selector=lambda source_element, collection_element: (source_element, collection_element)))

         .. rubric:: Example

         Incorporate each album track with its performing artist into a
         descriptive string::

           >>> albums = [dict(name="Hotel California", artist="The Eagles",
           ...                tracks=["Hotel California",
           ...                        "New Kid in Town",
           ...                        "Life in the Fast Lane",
           ...                        "Wasted Time"]),
           ...           dict(name="Revolver", artist="The Beatles",
           ...                tracks=["Taxman",
           ...                        "Eleanor Rigby",
           ...                        "Yellow Submarine",
           ...                        "Doctor Robert"]),
           ...           dict(name="Thriller", artist="Michael Jackson",
           ...                tracks=["Thriller",
           ...                        "Beat It",
           ...                        "Billie Jean", 
           ...                        "The Girl Is Mine"])]
           >>> asq(albums).select_many_with_correspondence(lambda album: album['tracks'],
           ...   lambda album, track: track + " by " + album['artist']).to_list()
           ['Hotel California by The Eagles', 'New Kid in Town by The Eagles',
            'Life in the Fast Lane by The Eagles', 'Wasted Time by The Eagles',
            'Taxman by The Beatles', 'Eleanor Rigby by The Beatles',
            'Yellow Submarine by The Beatles', 'Doctor Robert by The Beatles',
            'Thriller by Michael Jackson', 'Beat It by Michael Jackson',
            'Billie Jean by Michael Jackson',
            'The Girl Is Mine by Michael Jackson']

      .. automethod:: select_many_with_index(collection_selector=lambda index, source_element: (index, source_element), result_selector=lambda source_element, collection_element: collection_element)

         .. rubric:: Example

         Incorporate the index of each album along with the track and artist
         for a digital jukebox. A generator expression is used to combine the
         index with the track name when generating the intermediate sequences
         from each album which will be concatenated into the final result::

           >>> albums = [dict(name="Hotel California", artist="The Eagles",
           ...                tracks=["Hotel California",
           ...                        "New Kid in Town",
           ...                        "Life in the Fast Lane",
           ...                        "Wasted Time"]),
           ...           dict(name="Revolver", artist="The Beatles",
           ...                tracks=["Taxman",
           ...                        "Eleanor Rigby",
           ...                        "Yellow Submarine",
           ...                        "Doctor Robert"]),
           ...           dict(name="Thriller", artist="Michael Jackson",
           ...                tracks=["Thriller",
           ...                        "Beat It",
           ...                        "Billie Jean",
           ...                        "The Girl Is Mine"])]
           >>> asq(albums).select_many_with_index(lambda index, album: (str(index) + ' - ' + track for track in album['tracks'])).to_list()
           ['0 - Hotel California', '0 - New Kid in Town',
            '0 - Life in the Fast Lane', '0 - Wasted Time', '1 - Taxman',
            '1 - Eleanor Rigby', '1 - Yellow Submarine', '1 - Doctor Robert',
            '2 - Thriller', '2 - Beat It', '2 - Billie Jean',
            '2 - The Girl Is Mine']

         Incorporate the index of each album along with the track and artist
         for a digital jukebox. A generator expression is to define the
         collection_selector used to combine the index with the track name
         when generating the intermediate sequences from each album which will
         be concatenated into the final result::

           >>> albums = [dict(name="Hotel California", artist="The Eagles",
           ...                tracks=["Hotel California",
           ...                        "New Kid in Town",
           ...                        "Life in the Fast Lane",
           ...                        "Wasted Time"]),
           ...           dict(name="Revolver", artist="The Beatles",
           ...                tracks=["Taxman",
           ...                        "Eleanor Rigby",
           ...                        "Yellow Submarine",
           ...                        "Doctor Robert"]),
           ...           dict(name="Thriller", artist="Michael Jackson",
           ...                tracks=["Thriller",
           ...                        "Beat It",
           ...                        "Billie Jean",
           ...                        "The Girl Is Mine"])]
           >>> asq(albums).select_many_with_index(collection_selector=lambda index, album: (str(index) + ' - ' + track for track in album['tracks']),
           ...     result_selector=lambda album, track: album['name'] + ' - ' + track).to_list()
           ['Hotel California - 0 - Hotel California',
            'Hotel California - 0 - New Kid in Town',
            'Hotel California - 0 - Life in the Fast Lane',
            'Hotel California - 0 - Wasted Time', 'Revolver - 1 - Taxman',
            'Revolver - 1 - Eleanor Rigby', 'Revolver - 1 - Yellow Submarine',
            'Revolver - 1 - Doctor Robert', 'Thriller - 2 - Thriller',
            'Thriller - 2 - Beat It', 'Thriller - 2 - Billie Jean',
            'Thriller - 2 - The Girl Is Mine']

      .. automethod:: select_with_index(selector=lambda index, element: (index, element)

         .. rubric:: Examples

         Generate a list of 2-tuple pairs consisting of the element index and
         the element value using the default selector::
         
           >>> dark_side_of_the_moon = [ 'Speak to Me', 'Breathe', 'On the Run',
           ... 'Time', 'The Great Gig in the Sky', 'Money', 'Us and Them',
           ... 'Any Colour You Like', 'Brain Damage', 'Eclipse']
           >>> asq(dark_side_of_the_moon).select_with_index().to_list()
           [(0, 'Speak to Me'), (1, 'Breathe'), (2, 'On the Run'), (3, 'Time'),
            (4, 'The Great Gig in the Sky'), (5, 'Money'), (6, 'Us and Them'),
            (7, 'Any Colour You Like'), (8, 'Brain Damage'), (9, 'Eclipse')]

         Generate numbered album tracks using a custom selector::
         
           >>> asq(dark_side_of_the_moon).select_with_index(lambda index, track: str(index) + '. ' + track).to_list()
           ['0. Speak to Me', '1. Breathe', '2. On the Run', '3. Time',
            '4. The Great Gig in the Sky', '5. Money', '6. Us and Them',
            '7. Any Colour You Like', '8. Brain Damage', '9. Eclipse']
            
      .. automethod:: sequence_equal(second_iterable, equality_comparer=operator.eq)

         .. rubric:: Examples

         Determine whether lists ``a`` and ``b`` are equal::

           >>> a = [1, 3, 6, 2, 8]
           >>> b = [3, 6, 2, 1, 8]
           >>> asq(a).sequence_equal(b)
           False

         Determine whether lists ``a`` and ``b`` and equal when absolute values
         are compared::

           >>> a = [1, -3, 6, -2, 8]
           >>> b = [-1, 3, -6, 2, -8]
           >>> asq(a).sequence_equal(b, lambda lhs, rhs: abs(lhs) == abs(rhs))
           True

      .. automethod:: single(predicate=None)

         .. rubric:: Examples

         Return the only element in the sequence::

           >>> a = [5]
           >>> asq(a).single()
           5

         Attempt to get the single element from a sequence with multiple
         elements::

           >>> a = [7, 5, 4]
           >>> asq(a).single()
           ValueError: Sequence for single() contains multiple elements.

         Return the only element in a sequence meeting a condition::

           >>> a = [7, 5, 4]
           >>> asq(a).single(lambda x: x > 6)
           7

         Attempt to get the single element from a sequence which meets a
         condition when in fact multiple elements do so::

           >>> a = [7, 5, 4]
           >>> asq(a).single(lambda x: x >= 5)
           ValueError: Sequence contains more than one value matching single()
           predicate.
            
      .. automethod:: single_or_default(default, predicate=None)

         .. rubric:: Examples

         Return the only element in the sequence::

           >>> a = [5]
           >>> asq(a).single_or_default(7)
           5

         Attempt to get the single element from a sequence with *multiple*
         elements::

           >>> a = [7, 5, 4]
           >>> asq(a).single_or_default(9)
           ValueError: Sequence for single_or_default() contains multiple
           elements

         Attempt to get the single element from a sequence with *no* elements::

           >>> a = []
           >>> asq(a).single_or_default(9)
           9

         Return the only element in a sequence meeting a condition::

           >>> a = [7, 5, 4]
           >>> asq(a).single_or_default(9, lambda x: x > 6)
           7

         Attempt to get the single element from a sequence which meets a
         condition when in fact multiple elements do so::

           >>> a = [7, 5, 4]
           >>> asq(a).single(lambda x: x >= 5)
           ValueError: Sequence contains more than one value matching
           single_or_default() predicate.

         Attempt to get the single element matching a predicate from a sequence
         which contains no matching elements::

           >>> a = [7, 5, 4]
           >>> asq(a).single_or_default(9, lambda x: x > 20)
           9

      .. automethod:: skip(count=1)

         .. rubric:: Examples

         Skip the first element of a sequence::

           >>> a = [7, 5, 4]
           >>> asq(a).skip().to_list()
           [5, 4]

         Skip the first two elements of a sequence::

           >>> a = [7, 5, 4]
           >>> asq(a).skip(2).to_list()
           [4]

      .. automethod:: skip_while(predicate)

         .. rubric:: Example

         Skip while elements start with the letter 'a'::

           >>> words = ['aardvark', 'antelope', 'ape', 'baboon', 'cat',
           ...          'anaconda', 'zebra']
           >>> asq(words).skip_while(lambda s: s.startswith('a')).to_list()
           ['baboon', 'cat', 'anaconda', 'zebra']

      .. automethod:: sum(selector=identity)

         .. rubric:: Examples

         Compute the sum of a sequence of floats::

           >>> numbers = [5.6, 3.4, 2.3, 9.3, 1.7, 2.4]
           >>> asq(numbers).sum()
           24.7

         Compute the sum of the squares of a sequence of integers::

           >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
           >>> asq(numbers).sum(lambda x: x*x)
           385

      .. automethod:: take(count=1)

         .. rubric:: Examples

         Take one element from the start of a list::

           >>> a = [9, 7, 3, 4, 2]
           >>> asq(a).take().to_list()
           [9]

         Take three elements from the start of a list::

           >>> asq(a).take(3).to_list()
           [9, 7, 3]

      .. automethod:: take_while(predicate)

         .. rubric:: Example

         >>> words = ['aardvark', 'antelope', 'ape', 'baboon', 'cat',
         ...          'anaconda', 'zebra']
         >>> asq(words).take_while(lambda s: s.startswith('a')).to_list()
         ['aardvark', 'antelope', 'ape']

      .. automethod:: to_dictionary(key_selector=identity, value_selector=identity)

         .. rubric:: Examples

         Convert to a dictionary using the default key and value selectors::

           >>> animals = ['aardvark', 'baboon', 'cat', 'dot', 'frog', 'giraffe',
           ...            'horse', 'iguana']
           >>> asq(animals).to_dictionary()
           {'horse': 'horse', 'aardvark': 'aardvark', 'frog': 'frog', 'cat':
            'cat', 'giraffe': 'giraffe', 'baboon': 'baboon', 'dot': 'dot',
            'iguana': 'iguana'}

         Convert to a dictionary extracting the first letter as a key::

           >>> animals = ['aardvark', 'baboon', 'cat', 'dot', 'frog', 'giraffe',
           ...            'horse', 'iguana']
           >>> asq(animals).to_dictionary(key_selector=lambda x: x[0])
           {'a': 'aardvark', 'c': 'cat', 'b': 'baboon', 'd': 'dot', 'g':
            'giraffe', 'f': 'frog', 'i': 'iguana', 'h': 'horse'}

         Convert to a dictionary extracting the first letter as a key and
         converting the value to uppercase::

           >>> asq(animals).to_dictionary(key_selector=lambda x: x[0],
           ...                            value_selector=lambda x: x.upper())
           {'a': 'AARDVARK', 'c': 'CAT', 'b': 'BABOON', 'd': 'DOT', 'g':
            'GIRAFFE', 'f': 'FROG', 'i': 'IGUANA', 'h': 'HORSE'}

         Attempt to convert a list of fruit to a dictionary using the initial
         letter as the key, in the presence of a multiple keys of the same
         value::

           >>> fruit = ['apple', 'apricot', 'banana', 'cherry']
           >>> asq(fruit).to_dictionary(lambda f: f[0])
           ValueError: Duplicate key value 'a' in sequence during
           to_dictionary()

      .. automethod:: to_list()

         .. rubric:: Example

         Convert from a tuple into a list::

           >>> a = (1, 6, 8, 3, 4)
           >>> asq(a).to_list()
           [1, 6, 8, 3, 4]

      .. automethod:: to_lookup()

         .. rubric:: Examples

         Convert to a Lookup using the default key_selector and
         value_selector::

           >>> countries = ['Austria', 'Bahrain', 'Canada', 'Algeria',
           ...              'Belgium', 'Croatia', 'Kuwait', 'Angola', 'Greece',
           ...              'Korea']
           >>> asq(countries).to_lookup()
           Lookup([('Austria', 'Austria'), ('Bahrain', 'Bahrain'), ('Canada',
           'Canada'), ('Algeria', 'Algeria'), ('Belgium', 'Belgium'),
           ('Croatia', 'Croatia'), ('Kuwait', 'Kuwait'), ('Angola', 'Angola'),
           ('Greece', 'Greece'), ('Korea', 'Korea')])

         Convert to a Lookup, using the initial letter of each country name as
         the key::

           >>> countries = ['Austria', 'Bahrain', 'Canada', 'Algeria',
           ...              'Belgium', 'Croatia', 'Kuwait', 'Angola', 'Greece',
           ...              'Korea']
           >>> asq(countries).to_lookup(key_selector=lambda name: name[0])
           Lookup([('A', 'Austria'), ('A', 'Algeria'), ('A', 'Angola'), ('B',
           'Bahrain'), ('B', 'Belgium'), ('C', 'Canada'), ('C', 'Croatia'),
           ('K', 'Kuwait'), ('K', 'Korea'), ('G', 'Greece')])

         Convert to a Lookup, using the initial letter of each country name as
         the key and the upper case name as the value::

           >>> countries = ['Austria', 'Bahrain', 'Canada', 'Algeria',
           ...              'Belgium', 'Croatia', 'Kuwait', 'Angola', 'Greece',
           ...              'Korea']
           >>> asq(countries).to_lookup(key_selector=lambda name: name[0],
           ...                        value_selector=lambda name: name.upper())
           Lookup([('A', 'AUSTRIA'), ('A', 'ALGERIA'), ('A', 'ANGOLA'), ('B',
           'BAHRAIN'), ('B', 'BELGIUM'), ('C', 'CANADA'), ('C', 'CROATIA'),
           ('K', 'KUWAIT'), ('K', 'KOREA'), ('G', 'GREECE')])

      .. automethod:: to_set()

         .. rubric:: Examples

         Convert a list to a set::

           >>> a = [4, 9, 2, 3, 0, 1]
           >>> asq(a).to_set()
           {0, 1, 2, 3, 4, 9}

         Attempt to convert a list containing duplicates to a set::

           >>> b = [6, 2, 9, 0, 2, 1, 9]
           >>> asq(b).to_set()
           ValueError: Duplicate item value 2 in sequence during to_set()

      .. automethod:: to_str(separator)

         .. rubric:: Examples

         Convert a sequence of characters into a string::

         >>> chars = ['c', 'h', 'a', 'r', 'a', 'c', 't', 'e', 'r', 's']
         >>> asq(chars).to_str()
         'characters'

         Concatenate some word fragments into a single string::

           >>> syllables = ['pen', 'ta', 'syll', 'ab', 'ic']
           >>> asq(syllables).to_str()

         Coerce some integers to strings and concatenate their digits to form
         a single string::

           >>> codes = [72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33]
           >>> asq(codes).to_str('-')
           '72-101-108-108-111-44-32-87-111-114-108-100-33'

         Coerce some integers to strings and concatenate their values separated
         by hyphens to form a single string::

           >>> codes = [72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33]
           >>> asq(codes).to_str('-')
           '72-101-108-108-111-44-32-87-111-114-108-100-33'

      .. automethod:: to_tuple()

         .. rubric:: Example

         Convert from a list into a tuple::

           >>> a = [1, 6, 8, 3, 4]
           >>> asq(a).to_list()
           (1, 6, 8, 3, 4)

      .. automethod:: union(second_iterable, selector=identity)

         .. rubric:: Examples

         Create a list of numbers which are in either or both of two lists::

           >>> a = [1, 6, 9, 3]
           >>> b = [2, 6, 7, 3]
           >>> asq(a).union(b).to_list()
           [1, 6, 9, 3, 2, 7]

         Create a list of numbers, based on their absolute values, which are in
         either or both of list ``a`` or list ``b``, preferentially taking
         numbers from list ``a`` where the absolute value is present in both::

           >>> a = [-1, -4, 2, 6, 7]
           >>> b = [3, -4, 2, -6, 9]
           >>> asq(a).union(b, abs).to_list()
           [-1, -4, 2, 6, 7, 3, 9]

      .. automethod:: where(predicate)

         .. rubric:: Example

         Filter for elements greater than five::

           >>> a = [1, 7, 2, 9, 3]
           >>> asq(a).where(lambda x: x > 5).to_list()
           [7, 9]

      .. automethod:: zip(second_iterable, result_selector=lambda x, y: (x, y))

         .. rubric:: Examples

         Combine two sequences using the default result selector which creates
         a 2-tuple pair of corresponding elements::

           >>> a = [1, 4, 6, 4, 2, 9, 1, 3, 8]
           >>> b = [6, 7, 2, 9, 3, 5, 9]
           >>> asq(a).zip(b).to_list()
           [(1, 6), (4, 7), (6, 2), (4, 9), (2, 3), (9, 5), (1, 9)]

         Multiply the corresponding elements of two sequences to create a new
         sequence equal in length to the shorter of the two::

           >>> a = [1, 4, 6, 4, 2, 9, 1, 3, 8]
           >>> b = [6, 7, 2, 9, 3, 5, 9]
           >>> asq(a).zip(b, lambda x, y: x * y).to_list()
           [6, 28, 12, 36, 6, 45, 9]

OrderedQueryable
----------------

   .. autoclass:: OrderedQueryable

      .. autosummary::
         :nosignatures:

         .. currentmodule asq.queryable

Lookup
------

   .. autoclass:: Lookup

      .. autosummary::
         :nosignatures:

         .. currentmodule asq.queryable

Grouping
--------

   .. autoclass:: Grouping

      .. autosummary::
         :nosignatures:

         .. currentmodule asq.queryable




         

Parallel asq
============

Parallel asq uses Python's multiprocessing library to distribute the effort

.. automodule:: asq.parallel_queryable

   .. autoclass:: ParallelQueryable

      .. automethod:: select(selector=identity)

         .. rubric:: Example

         And now x for an example pertinent to ``select()``::

           asq(foo).select(lambda x: x * 2).to_list()

         There - wasn't that great!

      .. automethod:: select_with_index

