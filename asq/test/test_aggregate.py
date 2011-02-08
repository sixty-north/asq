import operator
import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestAggregate(unittest.TestCase):

    def test_aggregate(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).aggregate(operator.add)
        self.assertEqual(b, 55)

    def test_aggregate_seed(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).aggregate(operator.add, 5)
        self.assertEqual(b, 60)

    def test_aggregate_result_selector(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).aggregate(operator.add, result_selector=lambda x: x*2)
        self.assertEqual(b, 110)

    def test_aggregate_seed_result_selector(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).aggregate(operator.add, 5, lambda x: x*2)
        self.assertEqual(b, 120)

    def test_aggregate_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).aggregate(operator.add))

    def test_aggregate_empty_seed(self):
        b = Queryable([]).aggregate(operator.add, 67)
        self.assertEqual(b, 67)

    def test_aggregate_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.aggregate(operator.add, 72))
