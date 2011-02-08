import unittest
from asq.queryable import Lookup

__author__ = 'rjs'

class TestLookup(unittest.TestCase):

    def test_lookup_create(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)

    def test_lookup_create_invalid(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c',),
                ('b', 'blueberry'),
                ('c',),
                ('c', 'cantaloupe') ]

        self.assertRaises(ValueError, lambda: Lookup(k_v))

    def test_lookup_create_empty(self):
        k_v = []
        lookup = Lookup(k_v)

    def test_lookup_len(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        self.assertEqual(len(lookup), 3)

    def test_lookup_in_positive(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        self.assertTrue('a' in lookup)

    def test_lookup_in_positive(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        self.assertFalse('z' in lookup)

    def test_lookup_repr(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        self.assertEqual(repr(lookup), "Lookup([('a', 'artichoke'), ('b', 'blackberry'), ('b', 'blueberry'), ('c', 'clementine'), ('c', 'cranberry'), ('c', 'cantaloupe')])")


    def test_lookup_getitem(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        g_a = lookup['a']
        self.assertEqual(g_a.key, 'a')
        self.assertTrue('artichoke' in g_a)

        g_b = lookup['b']
        self.assertEqual(g_b.key, 'b')
        self.assertTrue('blackberry' in g_b)
        self.assertTrue('blueberry' in g_b)

        g_c = lookup['c']
        self.assertEqual(g_c.key, 'c')
        self.assertTrue('clementine' in g_c)
        self.assertTrue('cranberry' in g_c)
        self.assertTrue('cantaloupe' in g_c)

    def test_lookup_apply_result_selector_default(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        result = lookup.apply_result_selector().to_list()
        # TODO: How to test?

    def test_lookup_apply_result_selector_default(self):
        k_v = [ ('a', 'artichoke'),
                ('b', 'blackberry'),
                ('c', 'clementine'),
                ('b', 'blueberry'),
                ('c', 'cranberry'),
                ('c', 'cantaloupe') ]

        lookup = Lookup(k_v)
        result = lookup.apply_result_selector(lambda key, seq: key).to_list()
        self.assertEqual(len(result), 3)
        self.assertTrue('a' in result)
        self.assertTrue('b' in result)
        self.assertTrue('c' in result)
        



  