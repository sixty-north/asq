import unittest
from asq.queryables import Grouping

from asq._portability import OrderedDict

__author__ = 'rjs'

class TestGrouping(unittest.TestCase):

    def test_grouping_create(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12])

        grouping = Grouping(od, 'b')

    def test_grouping_create_invalid(self):
        od = 5
        self.assertRaises(TypeError, lambda: Grouping(od, 'x'))

    def test_grouping_len(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12, 13])

        b_grouping = Grouping(od, 'b')
        self.assertEqual(len(b_grouping), 4)

        c_grouping = Grouping(od, 'c')
        self.assertEqual(len(c_grouping), 5)

    def test_grouping_repr(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12, 13])

        b_grouping = Grouping(od, 'b')
        self.assertEqual(repr(b_grouping), "Grouping(key='b')")

        c_grouping = Grouping(od, 'c')
        self.assertEqual(repr(c_grouping), "Grouping(key='c')")

    def test_grouping_key(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12, 13])

        b_grouping = Grouping(od, 'b')
        self.assertEqual(b_grouping.key, 'b')

        c_grouping = Grouping(od, 'c')
        self.assertEqual(c_grouping.key, 'c')


    def test_grouping_iterable(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12, 13])

        b_grouping = Grouping(od, 'b')
        lst = []
        for item in b_grouping:
            lst.append(item)
        self.assertEqual(lst, [5, 6, 7, 8])

    def test_grouping_as_queryable(self):
        od = OrderedDict(a=[1, 2, 3, 4],
                         b=[5, 6, 7, 8],
                         c=[9, 10, 11, 12, 13])

        b_grouping = Grouping(od, 'b')
        result = b_grouping.where(lambda x: x > 6).to_list()
        self.assertEqual(result, [7, 8])
        
