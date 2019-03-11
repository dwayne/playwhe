import datetime
import io
import unittest

from sqlalchemy import select

from playwhe.cli.store import Store, schema


class LoadTestCase(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.store.initialize()

    def tearDown(self):
        self.store = None

    def test_it_inserts_results(self):
        csvfile = io.StringIO('1,1994-07-04,AM,15\n2,1994-07-04,PM,11\n3,1994-07-05,AM,36\n4,1994-07-05,PM,31')
        self.store.load(csvfile)

        data = self.store.bind.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (1, datetime.date(1994, 7, 4), 'AM', 15))
        self.assertEqual(data[1], (2, datetime.date(1994, 7, 4), 'PM', 11))
        self.assertEqual(data[2], (3, datetime.date(1994, 7, 5), 'AM', 36))
        self.assertEqual(data[3], (4, datetime.date(1994, 7, 5), 'PM', 31))
