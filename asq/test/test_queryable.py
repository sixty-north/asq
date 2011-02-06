'''
test_queryable.py Unit tests for asq.queryable.Queryable
'''
import math

import unittest

from asq.queryable import Queryable, Lookup, Grouping

def times_two(x):
    return 2 * x

def times(x, y):
    return x * y

def infinite():
    i = 0
    while True:
        yield i
        i += 1

class TracingGenerator(object):

    def __init__(self):
        self._trace = []
        self._i = 0

    def __iter__(self):
        while True:
            self._trace.append(self._i)
            yield self._i
            self._i += 1

    trace = property(lambda self: self._trace)

class TestQueryable(unittest.TestCase):

    def test_non_iterable(self):
        self.assertRaises(TypeError, lambda: Queryable(5))
    
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
        a = ['Alice', 'Bob', 'Chris']
        b = Queryable(a).select_many_with_correspondence(list, lambda x, y: (x, y)).to_list()
        c = [('Alice', 'A'), ('Alice', 'l'), ('Alice', 'i'), ('Alice', 'c'), ('Alice', 'e'), ('Bob', 'B'), ('Bob', 'o'),
             ('Bob', 'b'), ('Chris', 'C'), ('Chris', 'h'), ('Chris', 'r'), ('Chris', 'i'), ('Chris', 's')]
        self.assertEqual(b, c)

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
        
    def test_where(self):
        a = range(0, 100)
        b = Queryable(a).where(lambda x: x % 3 == 0).to_list()
        c = list(range(0, 100, 3))
        self.assertEqual(b, c)
        

    def test_of_type(self):
        a = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        b = Queryable(a).of_type(int).to_list()
        c = [2, 3, 6, 8, 9]
        self.assertEqual(b, c)
        d = Queryable(a).of_type(str).to_list()
        e = ['one', 'four', 'five', 'seven', 'ten']
        self.assertEqual(d, e)

    def test_order_by(self):
        a = [1, 9, 7, 2, 5, 4, 6, 3, 8, 10]
        b = Queryable(a).order_by().to_list()
        c = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(b, c)

    def test_order_by_key(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a).order_by(len).to_list()
        c = ['by', 'Sort', 'words', 'length']
        self.assertEqual(b, c)

    def test_then_by(self):
        a = ['sort', 'these', 'words', 'by', 'length', 'and', 'then', 'lexicographically']
        b = Queryable(a).order_by(len).then_by().to_list()
        c = ['by', 'and', 'sort', 'then', 'these', 'words', 'length', 'lexicographically']
        self.assertEqual(b, c)

    def test_then_by_key(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2]).then_by(lambda y: y[1]).to_list()
        c = ['second', 'then', 'third', 'using', 'sort', 'letter']
        self.assertEqual(b, c)

    def test_order_by_descending(self):
        a = [1, 9, 7, 2, 5, 4, 6, 3, 8, 10]
        b = Queryable(a).order_by_descending().to_list()
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)

    def test_order_by_descending_key(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a).order_by_descending(len).to_list()
        c = ['length', 'words', 'Sort', 'by']
        self.assertEqual(b, c)

    def test_then_by_descending(self):
        a = ['sort', 'these', 'words', 'by', 'length', 'and', 'then', 'lexicographically']
        b = Queryable(a).order_by(len).then_by_descending().to_list()
        c = ['by', 'and', 'then', 'sort', 'words', 'these', 'length', 'lexicographically']
        self.assertEqual(b, c)

    def test_then_by_descending_key(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2]).then_by_descending(lambda y: y[1]).to_list()
        c = ['second', 'then', 'using', 'third', 'sort', 'letter']
        self.assertEqual(b, c)

    def test_take_negative(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take(-1).to_list()
        c = []
        self.assertEqual(b, c)

    def test_take_zero(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take(0).to_list()
        c = []
        self.assertEqual(b, c)

    def test_take_one(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).take().to_list()
        c = ['a']
        self.assertEqual(b, c)

    def test_take_five(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take(5).to_list()
        c = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(b, c)

    def test_take_too_many(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take(10).to_list()
        c = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.assertEqual(b, c)

    def test_take_from_infinite(self):
        b = Queryable(infinite()).take(5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_take_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).take()
        self.assertEqual(a.trace, [])
        c = b.to_list()
        self.assertEqual(a.trace, [0])

    def test_take_while(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).take_while(lambda x: x < 'e').to_list()
        c = ['a', 'b', 'c', 'd']
        self.assertEqual(b, c)

    def test_take_while_from_infinite(self):
        b = Queryable(infinite()).take_while(lambda x: x < 5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_take_while_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).take_while(lambda x: x < 3)
        self.assertEqual(a.trace, [])
        c = b.to_list()
        # 3 is included here in the trace because it must have been consumed in order to test
        # whether it satisfies the predicate
        self.assertEqual(a.trace, [0, 1, 2, 3])

    def test_skip_negative(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip(-1).to_list()
        c = ['a', 'b', 'c']
        self.assertEqual(b, c)

    def test_skip_zero(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip(0).to_list()
        c = ['a', 'b', 'c']
        self.assertEqual(b, c)

    def test_skip_one(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip().to_list()
        c = ['b', 'c']
        self.assertEqual(b, c)

    def test_skip_five(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).skip(5).to_list()
        c = ['f', 'g']
        self.assertEqual(b, c)

    def test_skip_too_many(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip(5).to_list()
        c = []
        self.assertEqual(b, c)

    def test_skip_from_infinite(self):
        b = Queryable(infinite()).skip(5).take().to_list()
        c = [5]
        self.assertEqual(b, c)

    def test_skip_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).skip(3)
        self.assertEqual(a.trace, [])
        c = b.take().to_list()
        self.assertEqual(c, [3])

    def test_concat(self):
        a = [1, 2, 3]
        b = Queryable(a).concat([4, 5, 6]).to_list()
        c = [1, 2, 3, 4, 5, 6]
        self.assertEqual(b, c)

    def test_concat_infinite(self):
        b = Queryable(infinite()).concat(infinite()).take(3).to_list()
        c = [0, 1, 2]
        self.assertEqual(b, c)

    def test_concat_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = TracingGenerator()
        self.assertEqual(b.trace, [])
        c = Queryable(a).concat(b).take().to_list()
        self.assertEqual(a.trace, [0])
        self.assertEqual(b.trace, [])

    def test_reverse(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).reverse().to_list()
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)

    def test_element_at(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        b = Queryable(a).element_at(3)
        self.assertEqual(b, 8)

    def test_element_at_out_of_range_infinite(self):
        self.assertRaises(ValueError, lambda: Queryable(infinite()).element_at(-1))

    def test_element_at_out_of_range(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        self.assertRaises(ValueError, lambda: Queryable(a).element_at(20))

    def test_element_at_infinite(self):
        b = Queryable(infinite()).element_at(5)
        self.assertEqual(b, 5)

    def test_count_empty_collection(self):
        b = Queryable([]).count()
        self.assertEqual(b, 0)

    def test_count_empty_sequence(self):
        def empty():
            if False:
                yield 0
        b = Queryable(empty()).count()
        self.assertEqual(b, 0)

    def test_count_finite_collection(self):
        a = [1, 2, 3]
        b = Queryable(a).count()
        self.assertEqual(b, 3)

    def test_count_finite_sequence(self):
        def seq():
            yield 1
            yield 2
            yield 3
        b = Queryable(seq()).count()
        self.assertEqual(b, 3)

    def test_any_empty(self):
        a = []
        b = Queryable(a).any()
        self.assertFalse(b)

    def test_any_not_empty(self):
        a = [False, False, False]
        b = Queryable(a).any()
        self.assertTrue(b)

    def test_any_negative_predicate(self):
        a = [1, 2, 3, 4, 8, 34]
        b = Queryable(a).any(lambda x: x == 15)
        self.assertFalse(b)

    def test_any_positive_predicate(self):
        a = [1, 2, 3, 4, 8, 34]
        b = Queryable(a).any(lambda x: x == 8)
        self.assertTrue(b)

    def test_any_infinite(self):
        b = Queryable(infinite()).any()
        self.assertTrue(b)

    def test_any_infinite_predicate(self):
        b = Queryable(infinite()).any(lambda x: x == 1000)

    def test_all_positive(self):
        a = [True, True, True, True]
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_negative(self):
        a = [True, True, True, False]
        b = Queryable(a).all()
        self.assertFalse(b)

    def test_all_empty(self):
        a = []
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_min(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min()
        self.assertEqual(b, -8)

    def test_min_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min(abs)
        self.assertEqual(b, 1)

    def test_min_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).min())

    def test_max(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).max()
        self.assertEqual(b, 9)

    def test_max_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        b = Queryable(a).max(abs)
        self.assertEqual(b, 13)

    def test_max_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).max())

    def test_sum(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).sum()
        self.assertEqual(b, 26)

    def test_sum_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        b = Queryable(a).sum(abs)
        self.assertEqual(b, 53)

    def test_sum_empty(self):
        b = Queryable([]).sum()
        self.assertEqual(b, 0)

    def test_average(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 3]
        b = Queryable(a).average()
        self.assertEqual(b, 2)

    def test_average_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).average(abs)
        self.assertEqual(b, 5)

    def test_average_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).average())

    def test_contains_positive(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(2)
        self.assertTrue(b)

    def test_contains_negative(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(6)
        self.assertFalse(b)

    def test_contains_empty(self):
        b = Queryable([]).contains(7)
        self.assertFalse(b)

    def test_default_if_empty_empty(self):
        b = Queryable([]).default_if_empty(5).to_list()
        self.assertEqual(b, [5])

    def test_default_if_empty_non_empty(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).default_if_empty(42).to_list()
        self.assertEqual(b, a)

    def test_default_if_empty_infinite(self):
        b = Queryable(infinite()).default_if_empty(42).take(5).to_list()
        self.assertEqual(b, [0, 1, 2, 3, 4])

    def test_distinct(self):
        a = [5, 7, -3, 2, 1, 5, 3, 2, 1, -15, 7]
        b = Queryable(a).distinct().to_list()
        c = [5, 7, -3, 2, 1, 3, -15]
        self.assertEqual(b, c)

    def test_distinct_selector(self):
        a = [5, 7, -3, 2, 1, 5, 3, 2, 1, -15, 7]
        b = Queryable(a).distinct(abs).to_list()
        c = [5, 7, -3, 2, 1, -15]
        self.assertEqual(b, c)

    def test_distinct_empty(self):
        b = Queryable([]).distinct().to_list()
        self.assertEqual(b, [])

    def test_distinct_infinite(self):
        b = Queryable(infinite()).distinct().take(5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_empty_singleton(self):
        self.assertTrue(Queryable.empty() is Queryable.empty())

    def test_empty_count(self):
        self.assertEqual(Queryable.empty().count(), 0)

    def test_difference(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).difference(b).to_list()
        d = [1, 3, 5, 6, 7, 8]
        self.assertEqual(c, d)

    def test_difference_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).difference(b))

    def test_difference_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).difference(b).to_list()
        d = [1, 2, 3, 4, 5]
        self.assertEqual(c, d)

    def test_difference_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, 8]
        c = Queryable(a).difference(b, abs).to_list()
        d = [1, 3, 6, 7]
        self.assertEqual(c, d)

    def test_difference_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).difference(b).take(10).to_list()
        d = [0, 1, 4, 5, 6, 8, 11, 12, 13, 14]
        self.assertEqual(c, d)

    def test_difference_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).difference(b)
        self.assertEqual(a.trace, [])
        d = c.take(10).to_list()
        e = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.assertEqual(a.trace, e)

    def test_difference_distinct(self):
        a = [1, 1, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).difference(b).to_list()
        d = [1, 4, 3]
        self.assertEqual(c, d)

    def test_intersect(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).intersect(b).to_list()
        d = [2, 4]
        self.assertEqual(c, d)

    def test_intersect_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).intersect(b))

    def test_intersect_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).intersect(b).to_list()
        d = []
        self.assertEqual(c, d)

    def test_intersect_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, 8]
        c = Queryable(a).intersect(b, abs).to_list()
        d = [2, 4, -5, -8]
        self.assertEqual(c, d)

    def test_intersect_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).intersect(b).take(5).to_list()
        d = [2, 3, 7, 9, 10]
        self.assertEqual(c, d)

    def test_intersect_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).intersect(b)
        self.assertEqual(a.trace, [])
        d = c.take(5).to_list()
        e = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(a.trace, e)

    def test_intersect_distinct(self):
        a = [1, 1, 2, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).intersect(b).to_list()
        d = [2, 5]
        self.assertEqual(c, d)

    def test_union(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        self.assertEqual(c, d)

    def test_union_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).union(b))

    def test_union_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(c, d)

    def test_union_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, -9]
        c = Queryable(a).union(b, abs).to_list()
        d = [1, 2, 3, 4, -5, 6 , 7, -8, -9]
        self.assertEqual(c, d)

    def test_union_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).union(b).take(5).to_list()
        d = [0, 1, 2, 3, 4]
        self.assertEqual(c, d)

    def test_union_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).union(b)
        self.assertEqual(a.trace, [])
        d = c.take(5).to_list()
        e = [0, 1, 2, 3, 4]
        self.assertEqual(a.trace, e)

    def test_union_distinct(self):
        a = [1, 1, 2, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 4, 5, 3]
        self.assertEqual(c, d)


    # TODO: Test each function with an empty sequence
    # TODO: Test each function with an infinite sequence

def inc_chr(y):
    return chr(ord(y)+1)

def randgen():
    import random
    while True:
        yield random.random()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueryable)
    unittest.TextTestRunner(verbosity=2).run(suite)
