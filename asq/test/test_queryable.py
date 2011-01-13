'''
test_queryable.py Unit tests for slinqer.Queryable
'''

import unittest

from asq.queryable import Queryable, identity
from asq.parallel_queryable import ParallelQueryable

def identity(x):
    return x

def times_two(x):
    return 2 * x

def times(x, y):
    return x * y

class TestQueryable(unittest.TestCase):

    def test_to_tuple(self):
        a = (27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4)
        b = Queryable(a).to_tuple()
        self.assertEqual(a, b)

    def test_to_list(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).to_list()
        self.assertEqual(a, b)

    def test_select(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).select(lambda x: x*2).to_list()
        c = [54, 148, 36, 96, 114, 194, 152, 40, 182, 16, 160, 118, 40, 64, 116, 24, 148, 156, 8]
        self.assertEqual(b, c)

    def test_select_empty(self):
        a = []
        b = Queryable(a).select(lambda x: x*2).to_list()
        self.assertEqual(a, b)

    def test_select_with_index_finite(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).select_with_index(lambda x, y: x*y).to_list()
        c = [0, 74, 36, 144, 228, 485, 456, 140, 728, 72, 800, 649, 240, 416, 812, 180, 1184, 1326, 72]
        self.assertEqual(b, c)

    def test_select_many_projector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        b = Queryable(a).select_many(lambda x : x).to_list()
        c = ['f', 'o', 'x', 'k', 'a', 'n', 'g', 'a', 'r', 'o', 'o', 'b', 'i', 's', 'o', 'n', 'b', 'e', 'a', 'r']
        self.assertEqual(b, c)

    def test_select_many_projector_selector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        b = Queryable(a).select_many(lambda x : x, lambda y: chr(ord(y)+1)).to_list()
        c = ['g', 'p', 'y', 'l', 'b', 'o', 'h', 'b', 's', 'p', 'p', 'c', 'j', 't', 'p', 'o', 'c', 'f', 'b', 's']
        self.assertEqual(b, c)

    def test_order_by(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).order_by().to_list()
        c = [4, 8, 12, 18, 20, 20, 27, 32, 48, 57, 58, 59, 74, 74, 76, 78, 80, 91, 97]
        self.assertEqual(b, c)

    def test_select_many_with_index_projector(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        b = Queryable(a).select_many_with_index(lambda i, x: [str(i) + flower for flower in x['flowers']]).to_list()
        c = ['0Agapanthus', '0Allium', '0Alpina', '0Alstroemeria', '0Amaranthus', '0Amarylis', '1Bouvardia',
             '2Carnations', '2Cattleya', '2Celosia', '2Chincherinchee', '2Chrysanthemum']
        self.assertEqual(b, c)

    def test_select_many_with_index_projector_selector(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        b = Queryable(a).select_many_with_index(lambda i, x: [str(i) + flower for flower in x['flowers']],
                                                lambda y: y[:2]).to_list()
        c = ['0A', '0A', '0A', '0A', '0A', '0A', '1B', '2C', '2C', '2C', '2C', '2C']
        self.assertEqual(b, c)

    def test_select_many_with_correspondence(self):
        a = [{'name' : 'Alice', 'flowers' : ['Agapanthus', 'Allium', 'Alpina', 'Alstroemeria', 'Amaranthus', 'Amarylis' ] },
             {'name' : 'Bob',   'flowers' : ['Bouvardia' ]},
             {'name' : 'Chris', 'flowers' : ['Carnations', 'Cattleya', 'Celosia', 'Chincherinchee', 'Chrysanthemum']}]
        b = Queryable(a).select_many_with_correspondence(selector=lambda x, y: x + ' - ' + y).to_list()
        c = ['Alice - Agapanthus', 'Alice - Allium', 'Alice - Alpina', 'Alice - Alstroemeria', 'Alice - Amaranthus',
             'Alice - Amarylis', 'Bob - Bouvardia', 'Chris - Carnations', 'Chris - Cattleya', 'Chris - Celosia',
             'Chris - Chincherinchee', 'Chris - Chrysanthemum']
        self.assertEqual(b, c)

    # TODO: Test each function with an empty sequence
    # TODO: Test each function with an infinite sequence

class TestParallelQueryable(unittest.TestCase):

    def test_parallel_select(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        with Queryable(a) as q:
            b = q.as_parallel().select(times_two).to_list()    
        c = [54, 148, 36, 96, 114, 194, 152, 40, 182, 16, 160, 118, 40, 64, 116, 24, 148, 156, 8]
        self.assertEqual(len(b), len(c))
        self.assertEqual(set(b), set(c))

    def test_parallel_select_with_index_finite(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        with Queryable(a) as q:
            b = q.as_parallel().select_with_index(times).to_list()
        c = [0, 74, 36, 144, 228, 485, 456, 140, 728, 72, 800, 649, 240, 416, 812, 180, 1184, 1326, 72]
        self.assertEqual(len(b), len(c))
        self.assertEqual(set(b), set(c))

    def test_parallel_select_many_projector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        with Queryable(a) as q:
            b = q.as_parallel().select_many(identity).to_list()
        c = ['f', 'o', 'x', 'k', 'a', 'n', 'g', 'a', 'r', 'o', 'o', 'b', 'i', 's', 'o', 'n', 'b', 'e', 'a', 'r']
        self.assertEqual(sorted(b), sorted(c))

    def test_parallel_select_many_projector_selector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        with Queryable(a) as q:
            b = q.as_parallel().select_many(identity, inc_chr).to_list()
        c = ['g', 'p', 'y', 'l', 'b', 'o', 'h', 'b', 's', 'p', 'p', 'c', 'j', 't', 'p', 'o', 'c', 'f', 'b', 's']
        self.assertEqual(len(b), len(c))
        self.assertEqual(set(b), set(c))

    def test_parallel_order_by(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        with Queryable(a) as q:
            b = q.as_parallel().order_by().to_list()
        c = [4, 8, 12, 18, 20, 20, 27, 32, 48, 57, 58, 59, 74, 74, 76, 78, 80, 91, 97]
        self.assertEqual(b, c)

    #def test_parallel_order_by(self):
    #    with Queryable(randgen()) as q:
    #        a = q.as_parallel().take(1000000).order_by().to_list

def inc_chr(y):
    return chr(ord(y)+1)

def randgen():
    import random
    while True:
        yield random.random()

if __name__ == '__main__':
    unittest.main()
