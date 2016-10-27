import unittest
from asq.queryables import Queryable

__author__ = "Sixty North"


class TestAverage(unittest.TestCase):

    def test_average(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 3]
        b = Queryable(a).average()
        self.assertEqual(b, 2)

    def test_average_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).average(abs)
        self.assertEqual(b, 5)

    def test_average_empty(self):
        with self.assertRaises(ValueError):
            Queryable([]).average()

    def test_average_selector_non_callable(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        with self.assertRaises(TypeError):
            Queryable(a).average("not callable")

    def test_average_closed(self):
        b = Queryable([1])
        b.close()
        with self.assertRaises(ValueError):
            b.average()

