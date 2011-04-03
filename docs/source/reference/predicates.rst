Predicates
==========

.. automodule:: asq.predicates

  Predicates are boolean functions which return True or False.

  .. currentmodule asq.predicates

Predicate factories
-------------------

The predicate factories partially apply the binary comparison operators by
providing the right-hand-side argument.  The result is a unary function the
single argument to which is the left-hand-side of the comparison operator.

For example. the ``lt_(rhs)`` predicate factory returns::

  lambda lhs: lhs < rhs

where ``rhs`` is provided when the predicate is created but ``lhs`` takes the
value passed to the unary predicate.

  .. autosummary::
     :nosignatures:

     eq_
     in_
     is_
     ge_
     gt_
     le_
     lt_
     ne_

  .. autofunction:: eq_(rhs)

     .. rubric:: Example

     Filter for those numbers equal to five::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(eq_(5)).to_list()
       [5, 5]

  .. autofunction:: in_(lhs)

     .. rubric:: Example

     Filter for specific words containing 'ei'::

       >>> words = ['banana', 'receive', 'believe', 'ticket', 'deceive']
       >>> query(words).where(in_('ei')).to_list()
       ['receive', 'deceive']

  .. autofunction:: is_(rhs)

     .. rubric:: Example

     Filter for a specific object by identity::

       >>> sentinel = object()
       >>> sentinel
       <object object at 0x0000000002ED8040>
       >>> objects = ["Dinosaur", 5, sentinel, 89.3]
       >>> query(objects).where(is_(sentinel)).to_list()
       [<object object at 0x0000000002ED8040>]
       >>>

  .. autofunction:: ge_(rhs)

     .. rubric:: Example

     Filter for those numbers greater-than-or-equal to 43::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(ge_(43)).to_list()
       [89, 67, 43]

  .. autofunction:: gt_(rhs)

     .. rubric:: Example

     Filter for those numbers greater-than 43::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(gt_(43)).to_list()
       [89, 67]

  .. autofunction:: le_(rhs)

     .. rubric:: Example

     Filter for those numbers less-than-or-equal to 43::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(le_(43)).to_list()
       [5, 9, 12, 5, 34, 2, 43]

  .. autofunction:: lt_(rhs)

     .. rubric:: Example

     Filter for those numbers less-than-or-equal to 43::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(lt_(43)).to_list()
       [5, 9, 12, 5, 34, 2]

  .. autofunction:: ne_(rhs)

     .. rubric:: Example

     Filter for those numbers not equal to 5::

       >>> numbers = [5, 9, 12, 5, 89, 34, 2, 67, 43]
       >>> query(numbers).where(ne_(5)).to_list()
       [9, 12, 89, 34, 2, 67, 43]

Predicate combinators
---------------------

Predicate combinators allow the predicate factories to be modified and combined
in a concise way. For example, we can write::

  or_(lt_(5), gt_(37))

which will produce a predicate equivalent to::

  lambda lhs: lhs < 5 or lhs > 37

which can be applied to each element of a sequence to test whether the element
is outside the range 5 to 37.

  .. autosummary::
     :nosignatures:

     and_
     nand_
     nor_
     not_
     or_
     xnor_
     xor_

  .. autofunction:: and_(predicate1, predicate2)

     ..rubric:: Example

     Filter a list for all the words which both start with 'a' and end 't'::

       >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
       >>> query(words).where(and_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
       ['alphabet', 'aghast']

  ..  autofunction:: nand_(predicate1, predicate2)

      ..rubric:: Example

      Filter a list for all the words which don't both start and end with the
      letters 'a' and 't' respectively::

        >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
        >>> query(words).where(nand_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
        ['train', 'apple', 'tent', 'alarm']

  .. autofunction:: nor_(predicate1, predicate2)

     .. rubric:: Example

     Filter a list for all words which neither start with 'a' nor end with
     't'::

       >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
       >>> query(words).where(nor_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
       ['train']

  .. autofunction:: not_(predicate)

     .. rubric:: Example

     Filter a list for all the word which do not contain a specific sentinel
     object::

       >>> sentinel = object()
       >>> objects = ["Dinosaur", 5, sentinel, 89.3]
       >>> query(objects).where(not_(is_(sentinel))).to_list()
       ['Dinosaur', 5, 89.3]

  .. autofunction:: or_(predicate1, predicate2)

     .. rubric:: Example

     Filter a list for all words which either start with 'a' or end with 't'::

       >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
       >>> query(words).where(or_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
       ['alphabet', 'apple', 'aghast', 'tent', 'alarm']

  .. autofunction:: xor_(predicate1, predicate2)

     .. rubric:: Example

     Filter a list for all words which either start with 'a' or end with 't'
     but not both::

       >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
       >>> query(words).where(xor_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
       ['apple', 'tent', 'alarm']

  .. autofunction:: xnor_(predicate1, predicate2)

     .. rubric:: Example

     Filter a list for all words which, if they start with 'a' end with 't' or
     don't start with 'a' and don't end with 't'::

       >>> words = ['alphabet', 'train', 'apple', 'aghast', 'tent', 'alarm']
       >>> query(words).where(xnor_(m_('startswith', 'a'), m_('endswith', 't'))).to_list()
       ['alphabet', 'train', 'aghast']




