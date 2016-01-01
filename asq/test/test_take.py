import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

__author__ = "Sixty North"

class TestTake(unittest.TestCase):

    def test_take_negative(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take(-1).to_list()
        c = []
        self.assertEqual(b, c)

    def test_take_zero(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take(0).to_list()
        c = []
        self.assertEqual(b, c)

    def test_take_one(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take().to_list()
        c = ['a']
        self.assertEqual(b, c)

    def test_take_five(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take(5).to_list()
        c = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(b, c)

    def test_take_too_many(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take(10).to_list()
        c = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.assertEqual(b, c)

    def test_take_from_infinite(self):
        b = Queryable(infinite()).take(5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_take_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).take()
        self.assertEqual(a.trace, [])
        c = b.to_list()
        self.assertEqual(a.trace, [0])

    def test_take_closed(self):
        a = ['a', 'b', 'c']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.take(1))