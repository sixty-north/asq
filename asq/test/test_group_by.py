import unittest
from asq.queryables import Grouping, Queryable

__author__ = "Robert Smallshire"

class TestGroupBy(unittest.TestCase):

    def test_group_by(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a).group_by(lambda x: x[0]).to_list()
        self.assertEqual(len(b), 3)
        g1 = b[0]
        g2 = b[1]
        g3 = b[2]
        self.assertIsInstance(g1, Grouping)
        self.assertIsInstance(g2, Grouping)
        self.assertIsInstance(g3, Grouping)
        self.assertEqual(g1.to_list(), ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis'])
        self.assertEqual(g2.to_list(), ['Bouvardia'])
        self.assertEqual(g3.to_list(), ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum'])

    def test_group_by_key_selector_not_callable(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        self.assertRaises(TypeError, lambda: Queryable(a).group_by("not callable"))

    def test_element_selector(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a).group_by(key_selector=lambda x: x[0],
                                  element_selector=lambda x: x.lower()).to_list()
        self.assertEqual(len(b), 3)
        g1 = b[0]
        g2 = b[1]
        g3 = b[2]
        self.assertIsInstance(g1, Grouping)
        self.assertIsInstance(g2, Grouping)
        self.assertIsInstance(g3, Grouping)
        self.assertEqual(g1.to_list(), ['agapanthus', 'allium', 'alpina', 'alstroemeria', 'amaranthus', 'amarylis'])
        self.assertEqual(g2.to_list(), ['bouvardia'])
        self.assertEqual(g3.to_list(), ['carnations', 'cattleya', 'celosia', 'chincherinchee', 'chrysanthemum'])

    def test_element_selector_not_callable(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        self.assertRaises(TypeError, lambda: Queryable(a).group_by(key_selector=lambda x: x[0],
                                     element_selector="not callable"))


    def test_result_selector(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a).group_by(key_selector=lambda x: x[0],
                                  result_selector=lambda k, g: len(g)).to_list()
        self.assertEqual(len(b), 3)
        g1 = b[0]
        g2 = b[1]
        g3 = b[2]
        self.assertEqual(g1, 6)
        self.assertEqual(g2, 1)
        self.assertEqual(g3, 5)

    def test_result_selector_not_callable(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        self.assertRaises(TypeError, lambda: Queryable(a).group_by(key_selector=lambda x: x[0],
                                  result_selector="not callable"))

    def test_first_closed(self):
        a = ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis', 'Bouvardia', 'Carnations',
             'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.group_by(lambda x: x[0]))
