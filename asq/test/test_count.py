import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class TestCount(unittest.TestCase):

    def test_count_empty_collection(self):
        b = Queryable([]).count()
        self.assertEqual(b, 0)

    def test_count_empty_sequence(self):
        def empty():
            if False:
                yield 0
        b = Queryable(empty()).count()
        self.assertEqual(b, 0)

    def test_count_finite_collection(self):
        a = [1, 2, 3]
        b = Queryable(a).count()
        self.assertEqual(b, 3)

    def test_count_finite_sequence(self):
        def seq():
            yield 1
            yield 2
            yield 3
        b = Queryable(seq()).count()
        self.assertEqual(b, 3)

    def test_count_predicate(self):
        a = [1, 78, 45, 34, 98, 54, 53]
        b = Queryable(a).count(lambda x: x > 50)
        self.assertEqual(b, 4)

    def test_count_predicate_non_callable(self):
        a = [1, 78, 45, 34, 98, 54, 53]
        self.assertRaises(TypeError, lambda: Queryable(a).count("not callable"))
        
    def test_count_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.count())