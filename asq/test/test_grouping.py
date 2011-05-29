import unittest
from asq.queryables import Grouping

from asq._portability import OrderedDict

__author__ = 'rjs'

class TestGrouping(unittest.TestCase):

    def test_grouping_create(self):
        grouping = Grouping('b', [5, 6, 7, 8])

    def test_grouping_len(self):
        b_grouping = Grouping('b', [5, 6, 7, 8])
        self.assertEqual(len(b_grouping), 4)

        c_grouping = Grouping('c', [9, 10, 11, 12, 13])
        self.assertEqual(len(c_grouping), 5)

    def test_grouping_repr(self):
        b_grouping = Grouping('b', [5, 6, 7, 8])
        self.assertEqual(repr(b_grouping), "Grouping(key='b')")

        c_grouping = Grouping('c', [9, 10, 11, 12, 13])
        self.assertEqual(repr(c_grouping), "Grouping(key='c')")

    def test_grouping_key(self):
        b_grouping = Grouping('b', [5, 6, 7, 8])
        self.assertEqual(b_grouping.key, 'b')

        c_grouping = Grouping('c', [9, 10, 11, 12, 13])
        self.assertEqual(c_grouping.key, 'c')

    def test_grouping_iterable(self):
        b_grouping = Grouping('b', [5, 6, 7, 8])
        lst = []
        for item in b_grouping:
            lst.append(item)
        self.assertEqual(lst, [5, 6, 7, 8])

    def test_grouping_as_queryable(self):
        b_grouping = Grouping('b', [5, 6, 7, 8])
        result = b_grouping.where(lambda x: x > 6).to_list()
        self.assertEqual(result, [7, 8])

    def test_grouping_equal_positive(self):
        grouping1 = Grouping('b', [5, 6, 7, 8])
        grouping2 = Grouping('b', [5, 6, 7, 8])
        self.assertTrue(grouping1 == grouping2)

    def test_grouping_equal_negative_key(self):
        grouping1 = Grouping('a', [1, 2, 3, 4])
        grouping2 = Grouping('b', [1, 2, 3, 4])
        self.assertFalse(grouping1 == grouping2)

    def test_grouping_equal_negative_sequence(self):
        grouping1 = Grouping('a', [1, 2, 4, 3])
        grouping2 = Grouping('a', [1, 2, 3, 4])
        self.assertFalse(grouping1 == grouping2)

    def test_grouping_not_equal_negative(self):
        grouping1 = Grouping('b', [5, 6, 7, 8])
        grouping2 = Grouping('b', [5, 6, 7, 8])
        self.assertFalse(grouping1 != grouping2)

    def test_grouping_not_equal_positive_key(self):
        grouping1 = Grouping('a', [1, 2, 3, 4])
        grouping2 = Grouping('b', [1, 2, 3, 4])
        self.assertTrue(grouping1 != grouping2)

    def test_grouping_not_equal_positive_sequence(self):
        grouping1 = Grouping('a', [1, 2, 4, 3])
        grouping2 = Grouping('a', [1, 2, 3, 4])
        self.assertTrue(grouping1 != grouping2)

