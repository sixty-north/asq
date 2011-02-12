import unittest
from asq.queryable import Queryable

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

    def test_count_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.count())