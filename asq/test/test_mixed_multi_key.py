import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class TestMixedMultiKey(unittest.TestCase):

    def test_less_than_when_less_than(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        mmk2 = MixedMultiKey((1, 2, 2))
        self.assertTrue(mmk1 < mmk2)

    def test_less_than_when_greater_than(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        mmk2 = MixedMultiKey((1, 2, 4))
        self.assertFalse(mmk1 < mmk2)

    def test_less_than_when_equal(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        mmk2 = MixedMultiKey((1, 2, 3))
        self.assertFalse(mmk1 < mmk2)

    def test_equal_positive(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        mmk2 = MixedMultiKey((1, 2, 3))
        self.assertTrue(mmk1 == mmk2)

    def test_equal_negative(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        mmk2 = MixedMultiKey((1, 2, 4))
        self.assertFalse(mmk1 == mmk2)

    def test_repr(self):
        ordered_queryable = Queryable([1, 2, 3]).order_by()
        MixedMultiKey = ordered_queryable._create_mixed_multi_key(directions=(+1, -1, +1))
        mmk1 = MixedMultiKey((1, 2, 3))
        self.assertEqual(repr(mmk1), "MixedMultiKey((1, 2, 3))")


