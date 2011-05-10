import unittest
from asq.queryables import Queryable, Grouping

__author__ = 'rjs'

class TestToLookup(unittest.TestCase):

    def test_to_lookup(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a).to_lookup(lambda x: x[0])
        self.assertEqual(len(b), 3)
        g1 = b['A']
        g2 = b['B']
        g3 = b['C']
        self.assert_(isinstance(g1, Grouping))
        self.assert_(isinstance(g2, Grouping))
        self.assert_(isinstance(g3, Grouping))
        self.assertEqual(g1.to_list(), ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis'])
        self.assertEqual(g2.to_list(), ['Bouvardia'])
        self.assertEqual(g3.to_list(), ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum'])

    def test_to_lookup_key_selector(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_lookup(lambda x: x[0])
        self.assertEqual(len(b), 5)
        g1 = b['A']
        g2 = b['B']
        g3 = b['C']
        g4 = b['D']
        g5 = b['E']
        self.assert_(isinstance(g1, Grouping))
        self.assert_(isinstance(g2, Grouping))
        self.assert_(isinstance(g3, Grouping))
        self.assert_(isinstance(g4, Grouping))
        self.assert_(isinstance(g5, Grouping))
        self.assertEqual(g1.to_list(), ['Aardvark'])
        self.assertEqual(g2.to_list(), ['Balloon'])
        self.assertEqual(g3.to_list(), ['Carrot'])
        self.assertEqual(g4.to_list(), ['Daisy'])
        self.assertEqual(g5.to_list(), ['Ecological'])

    def test_to_lookup_key_selector_not_callable(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        self.assertRaises(TypeError, lambda: Queryable(a).to_lookup("not callable"))

    def test_to_lookup_value_selector(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_lookup(value_selector=len)
        self.assertEqual(len(b), 5)
        g1 = b['Aardvark']
        g2 = b['Balloon']
        g3 = b['Carrot']
        g4 = b['Daisy']
        g5 = b['Ecological']
        self.assert_(isinstance(g1, Grouping))
        self.assert_(isinstance(g2, Grouping))
        self.assert_(isinstance(g3, Grouping))
        self.assert_(isinstance(g4, Grouping))
        self.assert_(isinstance(g5, Grouping))
        self.assertEqual(g1.to_list(), [8])
        self.assertEqual(g2.to_list(), [7])
        self.assertEqual(g3.to_list(), [6])
        self.assertEqual(g4.to_list(), [5])
        self.assertEqual(g5.to_list(), [10])

    def test_to_lookup_value_selector(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        lambda: Queryable(a).to_lookup(value_selector="not callable")
        
    def test_to_lookup_duplicate_keys(self):
        a = ['Aardvark', 'Balloon', 'Baboon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_lookup(lambda x: x[0])
        self.assertEqual(len(b), 5)
        g1 = b['A']
        g2 = b['B']
        g3 = b['C']
        g4 = b['D']
        g5 = b['E']
        self.assert_(isinstance(g1, Grouping))
        self.assert_(isinstance(g2, Grouping))
        self.assert_(isinstance(g3, Grouping))
        self.assert_(isinstance(g4, Grouping))
        self.assert_(isinstance(g5, Grouping))
        self.assertEqual(g1.to_list(), ['Aardvark'])
        self.assertEqual(g2.to_list(), ['Balloon', 'Baboon'])
        self.assertEqual(g3.to_list(), ['Carrot'])
        self.assertEqual(g4.to_list(), ['Daisy'])
        self.assertEqual(g5.to_list(), ['Ecological'])

    def test_to_lookup_closed(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.to_lookup())
