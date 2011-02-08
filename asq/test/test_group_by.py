import unittest
from asq.queryable import Grouping, Queryable

__author__ = 'rjs'

class TestGroupBy(unittest.TestCase):

    def test_group_by(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a).group_by(lambda x: x[0]).to_list()
        self.assertEqual(len(b), 3)
        g1 = b[0]
        g2 = b[1]
        g3 = b[2]
        self.assert_(isinstance(g1, Grouping))
        self.assert_(isinstance(g2, Grouping))
        self.assert_(isinstance(g3, Grouping))
        self.assertEqual(g1.to_list(), ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis'])
        self.assertEqual(g2.to_list(), ['Bouvardia'])
        self.assertEqual(g3.to_list(), ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum'])
