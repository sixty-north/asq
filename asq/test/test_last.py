import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestLast(unittest.TestCase):

    def test_last(self):
        a = [42, 45, 23, 12]
        b = Queryable(a).last()
        self.assertEqual(b, 12)

    def test_last_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).last())

    def test_last_non_sequence(self):
        def series():
            yield 42
            yield 45
            yield 23
            yield 12
        a = series()
        b = Queryable(a).last()
        self.assertEqual(b, 12)

    def test_last_predicate_non_sequence(self):
        def series():
            yield 42
            yield 45
            yield 23
            yield 12
        a = series()
        b = Queryable(a).last(lambda x: x > 40)
        self.assertEqual(b, 45)

    def test_last_predicate(self):
        a = [37, 54, 57, 23, 12]
        b = Queryable(a).last(lambda x: x >= 50)
        self.assertEqual(b, 57)

    def test_last_predicate_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).last(lambda x: x >= 50))

    def test_last_predicate_missing(self):
        a = [37, 42, 23, 12]
        self.assertRaises(ValueError, lambda: Queryable(a).first(lambda x: x >= 50))

    def test_last_predicate_not_callable(self):
        a = [37, 54, 57, 23, 12]
        self.assertRaises(TypeError, lambda: Queryable(a).last("not callable"))
        
    def test_last_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.last())

  