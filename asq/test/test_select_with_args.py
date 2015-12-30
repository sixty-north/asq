import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite, TracingGenerator


class TestSelectWithIndex(unittest.TestCase):
    def test_select_with_args(self):
        a = [27, 74, 18, 48, 57, 97]
        b = Queryable(a).select_with_args(lambda x: x * 2).to_list()
        c = [(x, x * 2) for x in a]
        self.assertListEqual(b, c)

    def test_select_with_args_infinite(self):
        a = infinite()
        b = Queryable(a).select_with_args(lambda x: x * 2).take(4).to_list()
        c = [(x, x * 2) for x in range(4)]
        self.assertListEqual(b, c)

    def test_select_with_args_deferred(self):
        a = TracingGenerator()
        self.assertListEqual(a.trace, [])
        b = Queryable(a).select_with_args(lambda x: x * 2)
        self.assertListEqual(a.trace, [])
        b.take(3).to_list()
        self.assertListEqual(a.trace, list(range(3)))

    def test_select_with_args_not_callable(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        self.assertRaises(TypeError, lambda: Queryable(a).select_with_args("not callable"))

    def test_select_with_args_closed(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.select_with_args(lambda x: x * 2))

