import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestGroupJoin(unittest.TestCase):

    def test_group_join(self):
        a = [1, 2]
        b = [2, 3]
        c = Queryable(a).group_join(b).to_list()

        self.assertEqual(c[0].key, 1)
        self.assertEqual(len(c[0]), 0)

        self.assertEqual(c[1].key, 2)
        self.assertEqual(len(c[1]), 1)
        self.assertTrue(2 in c[1])

    def test_group_join_selectors(self):
        a = [1, 2, 3]
        b = ['a', 'I', 'to', 'of', 'be', 'are', 'one', 'cat', 'dog']
        c = Queryable(a).group_join(b, lambda outer: outer, lambda inner: len(inner),
                              lambda outer, inner: str(outer) + ':' + ','.join(inner)).to_list()
        d = ['1:a,I', '2:to,of,be', '3:are,one,cat,dog']
        self.assertEqual(c, d)

    def test_group_join_non_iterable(self):
        a = [1, 2, 3]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).group_join(b))

    def test_group_join_outer_selector_not_callable(self):
        a = [1, 2, 3]
        b = ['a', 'I', 'to', 'of', 'be', 'are', 'one', 'cat', 'dog']
        self.assertRaises(TypeError, lambda: Queryable(a).group_join(b, "not callable", lambda inner: len(inner),
                              lambda outer, inner: str(outer) + ':' + ','.join(inner)))

    def test_group_join_inner_selector_not_callable(self):
        a = [1, 2, 3]
        b = ['a', 'I', 'to', 'of', 'be', 'are', 'one', 'cat', 'dog']
        self.assertRaises(TypeError, lambda: Queryable(a).group_join(b, lambda outer: outer, "not callable",
                              lambda outer, inner: str(outer) + ':' + ','.join(inner)))

    def test_group_join_result_selector_not_callable(self):
        a = [1, 2, 3]
        b = ['a', 'I', 'to', 'of', 'be', 'are', 'one', 'cat', 'dog']
        self.assertRaises(TypeError, lambda: Queryable(a).group_join(b, lambda outer: outer, lambda inner: len(inner),
                              "not callable"))

    def test_group_join_infinite(self):
        a = infinite()
        b = [2, 3, 5]
        c = Queryable(a).group_join(b).take(3).to_list()

        self.assertEqual(c[0].key, 0)
        self.assertEqual(len(c[0]), 0)

        self.assertEqual(c[1].key, 1)
        self.assertEqual(len(c[1]), 0)

        self.assertEqual(c[2].key, 2)
        self.assertEqual(len(c[2]), 1)
        self.assertTrue(2 in c[2])
        

    def test_group_join_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [2, 3, 4, 5, 6]
        c = Queryable(a).group_join(b)
        self.assertEqual(a.trace, [])
        d = c.take(3).to_list()
