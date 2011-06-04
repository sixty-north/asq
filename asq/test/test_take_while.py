import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'


class TestTakeWhile(unittest.TestCase):

    def test_take_while(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take_while(lambda x: x < 'e').to_list()
        c = ['a', 'b', 'c', 'd']
        self.assertEqual(b, c)

    def test_take_while_from_infinite(self):
        b = Queryable(infinite()).take_while(lambda x: x < 5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_take_while_not_callable(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.assertRaises(TypeError, lambda: Queryable(a).take_while("not callable"))

    def test_take_while_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).take_while(lambda x: x < 3)
        self.assertEqual(a.trace, [])
        c = b.to_list()
        # 3 is included here in the trace because it must have been consumed in order to test
        # whether it satisfies the predicate
        self.assertEqual(a.trace, [0, 1, 2, 3])

    def test_take_while_closed(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.take_while(lambda x: x < 'e'))

    