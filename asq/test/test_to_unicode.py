import unittest
from asq._portability import has_unicode_type
from asq.queryables import Queryable

__author__ = "Sixty North"

if has_unicode_type():

    # This is done to keep PyCharm and various other Python test discovery
    # frameworks happy on Python 3.  They mostly ignore the preceding
    # conditional.

    u = unicode

    class TestToUnicode(unittest.TestCase):

        def test_to_unicode(self):
            a = u("This is a string")
            b = Queryable(a).to_unicode()
            self.assertEqual(a, b)

        def test_to_unicode_from_sequence(self):
            a = [u("This "), u("is "), u("a "), u("string!")]
            b = u("This is a string!")
            c = Queryable(a).to_unicode()
            self.assertEqual(b, c)

        def test_to_unicode_from_empty_sequence(self):
            a = []
            b = u("")
            c = Queryable(a).to_unicode()
            self.assertEqual(b, c)

        def test_to_unicode_empty_with_separator(self):
            a = []
            b = Queryable(a).to_unicode(separator=u(', '))
            c = u("")
            self.assertEqual(b, c)

        def test_to_unicode_one_with_separator(self):
            a = [u('string')]
            b = Queryable(a).to_unicode(separator=u(', '))
            c = u("string")
            self.assertEqual(b, c)

        def test_to_unicode_many_with_separator(self):
            a = [u('this'), u('list'), u('will'), u('be'), u('separated'), u('by'), u('semicolons')]
            b = Queryable(a).to_unicode(separator=u('; '))
            c = u("this; list; will; be; separated; by; semicolons")
            self.assertEqual(b, c)

        def test_to_unicode_stringify_separator(self):
            a = [u('this'), u('list'), u('will'), u('be'), u('separated'), u('by'), u('fives')]
            b = Queryable(a).to_unicode(separator=5)
            c = u("this5list5will5be5separated5by5fives")
            self.assertEqual(b, c)

        def test_stringify_items(self):
            a = [1, 5, 9, 34, 12, 3, 67, 1, 0]
            b = Queryable(a).to_unicode(separator=u(', '))
            c = u("1, 5, 9, 34, 12, 3, 67, 1, 0")
            self.assertEqual(b, c)

        def test_to_unicode_closed(self):
            a = [u('Aardvark'), u('Balloon'), u('Carrot'), u('Daisy'), u('Ecological')]
            b = Queryable(a)
            b.close()
            self.assertRaises(ValueError, lambda: b.to_unicode())
