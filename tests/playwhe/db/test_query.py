import datetime
import unittest

from sqlalchemy import create_engine

from playwhe.db.tasks import initialize
from playwhe.db.query import select_last_result
from playwhe.db.schema import results


class SelectLastResultTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        initialize(self.engine)

    def test_it_returns_last_result(self):
        with self.engine.begin() as conn:
            conn.execute(results.insert(), [
                { 'draw': 100, 'date': datetime.date(2000, 1, 1), 'period': 'EM', 'number': 1 },
                { 'draw': 101, 'date': datetime.date(2000, 1, 1), 'period': 'AM', 'number': 2 },
                { 'draw': 102, 'date': datetime.date(2000, 1, 1), 'period': 'AN', 'number': 3 },
                { 'draw': 103, 'date': datetime.date(2000, 1, 1), 'period': 'PM', 'number': 4 },
                { 'draw': 104, 'date': datetime.date(2000, 1, 2), 'period': 'EM', 'number': 5 },
                { 'draw': 105, 'date': datetime.date(2000, 1, 2), 'period': 'AM', 'number': 6 },
                { 'draw': 106, 'date': datetime.date(2000, 1, 2), 'period': 'AN', 'number': 7 },
                { 'draw': 107, 'date': datetime.date(2000, 1, 2), 'period': 'PM', 'number': 8 }
            ])

            last_result = conn.execute(select_last_result()).fetchone()

            self.assertEqual(last_result, (107, datetime.date(2000, 1, 2), 'PM', 8))

    def test_when_no_results(self):
        with self.engine.begin() as conn:
            last_result = conn.execute(select_last_result()).fetchone()

            self.assertIsNone(last_result)

    def test_when_draw_is_incorrect(self):
        with self.engine.begin() as conn:
            conn.execute(results.insert(), [
                { 'draw': 100, 'date': datetime.date(2000, 1, 1), 'period': 'EM', 'number': 1 },
                { 'draw': 102, 'date': datetime.date(2000, 1, 1), 'period': 'AN', 'number': 3 },
                { 'draw': 103, 'date': datetime.date(2000, 1, 1), 'period': 'PM', 'number': 4 },
                { 'draw': 104, 'date': datetime.date(2000, 1, 2), 'period': 'EM', 'number': 5 },
                { 'draw': 105, 'date': datetime.date(2000, 1, 2), 'period': 'AM', 'number': 6 },
                { 'draw': 106, 'date': datetime.date(2000, 1, 2), 'period': 'AN', 'number': 7 },
                { 'draw': 107, 'date': datetime.date(2000, 1, 2), 'period': 'PM', 'number': 8 },
                { 'draw': 201, 'date': datetime.date(2000, 1, 1), 'period': 'AM', 'number': 2 },
            ])

            last_result = conn.execute(select_last_result()).fetchone()

        self.assertEqual(last_result, (107, datetime.date(2000, 1, 2), 'PM', 8))
