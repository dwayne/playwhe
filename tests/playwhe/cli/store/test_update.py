import datetime
import unittest

from sqlalchemy import select

from playwhe.cli.store import Store, schema
from playwhe.common import Result, Results


FAKE_SERVER_RESULTS = {
    (1994, 7): [
        Result(1, 1994, 7, 4, 'AM', 36),
        Result(2, 1994, 7, 4, 'PM', 35),
        Result(3, 1994, 7, 5, 'AM', 34),
        Result(4, 1994, 7, 5, 'PM', 33)
    ],
    (1994, 8): [
        Result(5, 1994, 8, 1, 'AM', 32),
        Result(6, 1994, 8, 1, 'PM', 31)
    ]
}


def fake_fetch(year, month):
    try:
        results = FAKE_SERVER_RESULTS[(year, month)]
    except KeyError:
        results = []

    return Results(results)


class SyncTestCase(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.store.initialize()

    def tearDown(self):
        self.store = None

    def test_when_no_last_result(self):
        self.store.update(fetch=fake_fetch, today=lambda: datetime.date(1994, 10, 10))

        data = self.store.bind.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

        self.assertEqual(len(data), 6)
        self.assertEqual(data[0].draw, 1)
        self.assertEqual(data[1].draw, 2)
        self.assertEqual(data[2].draw, 3)
        self.assertEqual(data[3].draw, 4)
        self.assertEqual(data[4].draw, 5)
        self.assertEqual(data[5].draw, 6)

    def test_when_last_result(self):
        self.store.bind.execute(
            schema.results.insert(),
            [{ 'draw': 1, 'date': datetime.date(1994, 7, 31), 'period_abbr': 'PM', 'mark_number': 25 }]
        )

        self.store.update(fetch=fake_fetch, today=lambda: datetime.date(1994, 10, 10))

        data = self.store.bind.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0].draw, 1)
        self.assertEqual(data[1].draw, 5)
        self.assertEqual(data[2].draw, 6)
