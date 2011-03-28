Frequently Asked Questions
==========================

Where are ``map()``, ``filter()`` and ``reduce()``?
---------------------------------------------------

All three of these operators exist in ``asq`` with different spelling for
consistency with LINQ:

 ====================== ===============
 Python Standard Libary asq
 ====================== ===============
 ``map()``              ``select()``
 ``filter()``           ``where()``
 ``reduce()``           ``aggregate()``
 ====================== ===============

Where are ``fold()``, ``foldl()`` and ``foldr()``?
--------------------------------------------------

Folds in ``asq`` can be performed using ``aggregate()``. Here are the
equivalents of some Haskell code using folds and the Python ``asq`` code using
``aggregate()``:

 ====================  =====================================
 Haskell               asq
 ====================  =====================================
 ``foldl f seed seq``  ``asq(seq).aggregate(f, seed)``
 ``foldr f seed seq``  ``asq(seq).reverse().aggregate(f, seed)``
 ====================  =====================================

Wouldn't generators be a better name for what ``asq`` calls initiators?
-----------------------------------------------------------------------

Possibly, but it could be confused with other uses of the word 'generator' in
Python.  In fact, ``asq``'s initiators might actually *be* generators but the
essential point is that they 'initiate' the fluent query interface of ``asq``.

How do I pronounce ``asq``?
---------------------------

See the answer to the next question.

Where does the name ``asq`` come from?
--------------------------------------

Well, "asq" is homophonic with "ask" which is in turn synonymous with "query".
Further more, "query" contains a "q" which rather neatly takes us back to the
"q" in "asq". The inspiration for ``asq`` comes from "LINQ" where the "Q" also
stands for "query". Finally, the glyph "q" is mirror symmetric with "p" and
replacing the "q" in "asq" with "p" gives "asp" which also rhymes with "asq"
but more importantly is synonymous with "snake". "asq" is written in Python,
and pythons are a kind of snake, although the programming language is actually
named after a popular British comedy troupe and nothing to do with snakes at
all. Or something.





