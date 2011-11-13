import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

class TestToDictionary(unittest.TestCase):

    def test_to_dictionary(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_dictionary()
        c = {'Aardvark': 'Aardvark',
             'Balloon': 'Balloon',
             'Carrot': 'Carrot',
             'Daisy': 'Daisy',
             'Ecological': 'Ecological'}
        self.assertEqual(b, c)

    def test_to_dictionary_key_selector(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_dictionary(lambda x: x[0])
        c = {'A': 'Aardvark',
             'B': 'Balloon',
             'C': 'Carrot',
             'D': 'Daisy',
             'E': 'Ecological'}
        self.assertEqual(b, c)

    def test_to_dictionary_key_selector_not_callable(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        self.assertRaises(TypeError, lambda: Queryable(a).to_dictionary("not callable"))

    def test_to_dictionary_value_selector(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a).to_dictionary(value_selector=len)
        c = {'Aardvark': 8,
             'Balloon': 7,
             'Carrot': 6,
             'Daisy': 5,
             'Ecological': 10}
        self.assertEqual(b, c)

    def test_to_dictionary_value_selector_not_callable(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        self.assertRaises(TypeError, lambda:Queryable(a).to_dictionary(value_selector="not callable"))

    def test_to_dictionary_duplicate_keys(self):
        a = ['Aardvark', 'Balloon', 'Baboon', 'Carrot', 'Daisy', 'Ecological']
        self.assertRaises(ValueError, lambda: Queryable(a).to_dictionary(lambda x: x[0]))

    def test_to_dictionary_closed(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.to_dictionary())
        

