import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class Logger(object):

    def __init__(self):
        self.log = []

    def debug(self, message):
        self.log.append(message)

class TestLog(unittest.TestCase):

    def test_log_default(self):
        a = [1, 6, 4, 3, 9, 2]
        b = Queryable(a).log().to_list()
        self.assertEqual(a, b)

    def test_log_disable(self):
        a = [1, 6, 4, 3, 9, 2]
        b = Queryable(a).log(logger=None).to_list()
        self.assertEqual(a, b)

    def test_log_enable_deferred(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, eager=False).take(3).to_list()
        self.assertEqual(len(logger.log), 4)
        self.assertTrue(logger.log[0].find('BEGIN') != -1)
        self.assertTrue(logger.log[0].find('DEFERRED') != -1)
        self.assertTrue(logger.log[1].find('yields 1') != -1)
        self.assertTrue(logger.log[2].find('yields 6') != -1)
        self.assertTrue(logger.log[3].find('yields 4') != -1)

    def test_log_enable_eager(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, eager=True).to_list()
        self.assertEqual(len(logger.log), 8)
        self.assertTrue(logger.log[0].find('BEGIN') != -1)
        self.assertTrue(logger.log[0].find('EAGER') != -1)
        self.assertTrue(logger.log[1].find('= 1') != -1)
        self.assertTrue(logger.log[2].find('= 6') != -1)
        self.assertTrue(logger.log[3].find('= 4') != -1)
        self.assertTrue(logger.log[4].find('= 3') != -1)
        self.assertTrue(logger.log[5].find('= 9') != -1)
        self.assertTrue(logger.log[6].find('= 2') != -1)
        self.assertTrue(logger.log[7].find('END') != -1)

    def test_log_label_deferred(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="Test1", eager=False).take(3).to_list()
        for line in logger.log:
            self.assertTrue(line.startswith("Test1"))

    def test_log_label_eager(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="Test2", eager=True).to_list()
        for line in logger.log:
            self.assertTrue(line.startswith("Test2"))

    def test_log_interleaved_deferred(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="source") \
            .select(lambda x: x * 2).log(logger, label="times two") \
            .where(lambda x: x % 3).log(logger, label="mod three")  \
            .take(2).log(logger, label="take two").to_list()
        c = ['take two : BEGIN (DEFERRED)',
             'mod three : BEGIN (DEFERRED)',
             'times two : BEGIN (DEFERRED)',
             'source : BEGIN (DEFERRED)',
             'source : [0] yields 1',
             'times two : [0] yields 2',
             'mod three : [0] yields 2',
             'take two : [0] yields 2',
             'source : [1] yields 6',
             'times two : [1] yields 12',
             'source : [2] yields 4',
             'times two : [2] yields 8',
             'mod three : [1] yields 8',
             'take two : [1] yields 8',
             'take two : END (DEFERRED)']
        self.assertEqual(logger.log, c)

    def test_log_interleaved_eager(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="source", eager=True) \
            .select(lambda x: x * 2).log(logger, label="times two", eager=True) \
            .where(lambda x: x % 3).log(logger, label="mod three", eager=True)  \
            .take(2).log(logger, label="take two", eager=True).to_list()
        c = ['source : BEGIN (EAGER)',
             'source : [0] = 1',
             'source : [1] = 6',
             'source : [2] = 4',
             'source : [3] = 3',
             'source : [4] = 9',
             'source : [5] = 2',
             'source : END (EAGER)',
             'times two : BEGIN (EAGER)',
             'times two : [0] = 2',
             'times two : [1] = 12',
             'times two : [2] = 8',
             'times two : [3] = 6',
             'times two : [4] = 18',
             'times two : [5] = 4',
             'times two : END (EAGER)',
             'mod three : BEGIN (EAGER)',
             'mod three : [0] = 2',
             'mod three : [1] = 8',
             'mod three : [2] = 4',
             'mod three : END (EAGER)',
             'take two : BEGIN (EAGER)',
             'take two : [0] = 2',
             'take two : [1] = 8',
             'take two : END (EAGER)' ]
        self.assertEqual(logger.log, c)
