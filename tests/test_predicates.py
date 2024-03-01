import unittest
from asq.predicates import (eq_, ne_, lt_, le_, ge_, gt_, is_, contains_, not_,
                                and_, or_, xor_)
from asq.selectors import identity

__author__ = "Sixty North"

class TestEqual(unittest.TestCase):

    def test_positive(self):
        eq = eq_(5)
        self.assertTrue(eq(5))

    def test_negative(self):
        eq = eq_(37)
        self.assertFalse(eq(5))

class TestNotEqual(unittest.TestCase):

    def test_positive(self):
        ne = ne_(5)
        self.assertTrue(ne(37))

    def test_negative(self):
        ne = ne_(5)
        self.assertFalse(ne(5))

class TestLessThan(unittest.TestCase):

    def test_positive(self):
        lt = lt_(5)
        self.assertTrue(lt(4))

    def test_negative(self):
        lt = lt_(5)
        self.assertFalse(lt(5))

class TestLessThanOrEqual(unittest.TestCase):

    def test_positive_less(self):
        le = le_(5)
        self.assertTrue(le(4))

    def test_positive_equal(self):
        le = le_(5)
        self.assertTrue(le(5))

    def test_negative(self):
        le = le_(5)
        self.assertFalse(le(6))

class TestGreaterThanOrEqual(unittest.TestCase):

    def test_positive_greater(self):
        ge = ge_(5)
        self.assertTrue(ge(6))

    def test_positive_equal(self):
        ge = ge_(5)
        self.assertTrue(ge(5))

    def test_negative(self):
        gte = ge_(5)
        self.assertFalse(gte(4))

class TestGreaterThan(unittest.TestCase):

    def test_positive(self):
        gt = gt_(5)
        self.assertTrue(gt(6))

    def test_negative(self):
        gt = gt_(5)
        self.assertFalse(gt(5))

class TestIs(unittest.TestCase):

    def test_positive(self):
        sentinel = object()
        i = is_(sentinel)
        self.assertTrue(i(sentinel))

    def test_negative(self):
        sentinel1 = object()
        sentinel2 = object()
        i = is_(sentinel1)
        self.assertFalse(i(sentinel2))

class TestContains(unittest.TestCase):

    def test_positive(self):
        s = "The quick brown fox"
        f = contains_("fox")
        self.assertTrue(f(s))

    def test_negative(self):
        s = "The quick brown fox"
        f = contains_("sheep")
        self.assertFalse(f(s))

class TestNot(unittest.TestCase):

    def test_positive(self):
        n = not_(identity)
        self.assertTrue(n(False))

    def test_negative(self):
        n = not_(identity)
        self.assertFalse(n(True))

class TestAnd(unittest.TestCase):

    def test0(self):
        a = and_(not_(identity), not_(identity))
        self.assertFalse(a(True))

    def test1(self):
        a = and_(not_(identity), identity)
        self.assertFalse(a(True))

    def test2(self):
        a = and_(identity, not_(identity))
        self.assertFalse(a(True))

    def test3(self):
        a = and_(identity, identity)
        self.assertTrue(a(True))

class TestOr(unittest.TestCase):

    def test0(self):
        a = or_(not_(identity), not_(identity))
        self.assertFalse(a(True))

    def test1(self):
        a = or_(not_(identity), identity)
        self.assertTrue(a(True))

    def test2(self):
        a = or_(identity, not_(identity))
        self.assertTrue(a(True))

    def test3(self):
        a = or_(identity, identity)
        self.assertTrue(a(True))

class TestXor(unittest.TestCase):

    def test0(self):
        a = xor_(not_(identity), not_(identity))
        self.assertFalse(a(True))

    def test1(self):
        a = xor_(not_(identity), identity)
        self.assertTrue(a(True))

    def test2(self):
        a = xor_(identity, not_(identity))
        self.assertTrue(a(True))

    def test3(self):
        a = xor_(identity, identity)
        self.assertFalse(a(True))




