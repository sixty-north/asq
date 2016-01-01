import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

__author__ = "Sixty North"

class TestWhere(unittest.TestCase):

    def test_where(self):
        a = range(0, 100)
        b = Queryable(a).where(lambda x: x % 3 == 0).to_list()
        c = list(range(0, 100, 3))
        self.assertEqual(b, c)

    def test_where_not_callable(self):
        a = range(0, 100)
        self.assertRaises(TypeError, lambda: Queryable(a).where("not callable"))

    def test_where_infinite(self):
        a = infinite()
        b = Queryable(a).where(lambda x: x % 5 == 0).take(3).to_list()
        c = [0, 5, 10]
        self.assertEqual(b, c)

    def test_where_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).where(lambda x: x % 3 == 0)
        self.assertEqual(a.trace, [])
        c = b.take(2).to_list()
        self.assertEqual(a.trace, [0, 1, 2, 3])


    def test_where_closed(self):
        a = range(0, 100)
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.where(lambda x: x % 3 == 0))