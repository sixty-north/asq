import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

__author__ = 'rjs'

class TestJoin(unittest.TestCase):

    def test_join(self):
        a = [1, 2, 3, 4, 5]
        b = [4, 5, 6, 7, 8]
        c = Queryable(a).join(b).to_list()
        d = [(4, 4), (5, 5)]
        self.assertEqual(c, d)

    def test_join_selectors(self):
        a = [1, 2, 3]
        b = ['a', 'I', 'to', 'of', 'be', 'are', 'one', 'cat', 'dog']
        c = Queryable(a).join(b, lambda outer: outer, lambda inner: len(inner),
                              lambda outer, inner: str(outer) + ':' + inner).to_list()
        d = ['1:a', '1:I', '2:to', '2:of', '2:be', '3:are', '3:one', '3:cat', '3:dog']
        self.assertEqual(c, d)

    def test_join_non_iterable(self):
        a = [1, 2, 3]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).join(b))

    def test_join_infinite(self):
        a = infinite()
        b = [2, 3, 4, 5, 6]
        c = Queryable(a).join(b).take(3).to_list()
        d = [(2, 2), (3, 3), (4, 4)]
        self.assertEqual(c, d)

    def test_join_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [2, 3, 4, 5, 6]
        c = Queryable(a).join(b)
        self.assertEqual(a.trace, [])
        d = c.take(3).to_list()
        e = [(2, 2), (3, 3), (4, 4)]
        self.assertEqual(d, e)


