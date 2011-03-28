import unittest
from asq._portability import is_callable
from asq.selectors import k_, a_, m_, identity
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestKeySelector(unittest.TestCase):

    def test_k_result_is_callable(self):
        foo_selector = k_('foo')
        self.assertTrue(is_callable(foo_selector))

    def test_k_positive(self):
        d = {'sheila' : 56, 'jim' : 23, 'fred' : 55}
        jim_selector = k_('jim')
        self.assertEqual(jim_selector(d), 23)

    def test_k_negative(self):
        d = {'sheila' : 56, 'jim' : 23, 'fred' : 55}
        foo_selector = k_('foo')
        self.assertRaises(KeyError, lambda: foo_selector(d))

class TestAttributeSelector(unittest.TestCase):

    class HasAttributes(object):

        def __init__(self):
            self.sheila = 56
            self.jim = 23
            self.fred = 55

    def test_a_result_is_callable(self):
        foo_selector = a_('foo')
        self.assertTrue(is_callable(foo_selector))

    def test_a_positive(self):
        c = TestAttributeSelector.HasAttributes()
        jim_selector = a_('jim')
        self.assertEqual(jim_selector(c), 23)

    def test_a_negative(self):
        c = TestAttributeSelector.HasAttributes()
        foo_selector = a_('foo')
        self.assertRaises(AttributeError, lambda: foo_selector(c))

class TestMethodSelector(unittest.TestCase):

    class HasMethods(object):

        def sheila(self, arg1, arg2):
            return 56 + arg1 + arg2

        def jim(self):
            return 23

        def fred(self, arg1):
            return 55 + arg1

    def test_m_result_is_callable(self):
        foo_selector = m_('foo')
        self.assertTrue(is_callable(foo_selector))

    def test_m_positive(self):
        c = TestMethodSelector.HasMethods()
        jim_selector = m_('jim')
        self.assertEqual(jim_selector(c), 23)

    def test_m_negative(self):
        c = TestMethodSelector.HasMethods()
        foo_selector = m_('foo')
        self.assertRaises(AttributeError, lambda: foo_selector(c))

    def test_m_positional_args(self):
        c = TestMethodSelector.HasMethods()
        fred_selector = m_('fred', 45)
        self.assertEqual(fred_selector(c), 100)

    def test_m_named_args(self):
        c = TestMethodSelector.HasMethods()
        fred_selector = m_('sheila', arg2 = 45, arg1 = 33)
        self.assertEqual(fred_selector(c), 134)

class TestIdentity(unittest.TestCase):

    def test_identity(self):
        sentinel = object()
        self.assertTrue(identity(sentinel) is sentinel)