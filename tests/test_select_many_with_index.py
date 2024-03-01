import unittest
from asq.queryables import Queryable
from helpers import infinite, TracingGenerator

__author__ = "Sixty North"

class TestSelectManyWithIndex(unittest.TestCase):

    def test_select_many_with_index_collection_selector(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        b = Queryable(a).select_many_with_index(lambda i, x: [str(i) + flower for flower in x['flowers']]).to_list()
        c = ['0Agapanthus', '0Allium', '0Alpina', '0Alstroemeria', '0Amaranthus', '0Amarylis', '1Bouvardia',
             '2Carnations', '2Cattleya', '2Celosia', '2Chincherinchee', '2Chrysanthemum']
        self.assertEqual(b, c)

    def test_select_many_with_index_collection_selector_not_callable(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        self.assertRaises(TypeError, lambda: Queryable(a).select_many_with_index("not callable", lambda y: y[:2]))

    def test_select_many_with_index_result_selector_not_callable(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        self.assertRaises(TypeError, lambda: Queryable(a).select_many_with_index(lambda i, x: [str(i) + flower for flower in x['flowers']],
                                                "not callable"))

    def test_select_many_with_index_infinite(self):
        a = infinite()
        b = Queryable(a).select_many_with_index(lambda index, source_element: [source_element] * index).take(10).to_list()
        c = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        self.assertEqual(b, c)

    def test_select_many_with_index_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).select_many_with_index(lambda index, source_element: [source_element] * index)
        self.assertEqual(a.trace, [])
        b.take(10).to_list()
        self.assertEqual(a.trace, [0, 1, 2, 3, 4])

    def test_select_many_with_index_closed(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.select_many_with_index(lambda i, x: [str(i) + flower for flower in x['flowers']]))