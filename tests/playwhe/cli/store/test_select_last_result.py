import datetime
import unittest

from sqlalchemy import create_engine

from playwhe.cli.store import Store, schema, select_last_result


class SelectLastResultTestCase(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.store.initialize()

    def tearDown(self):
        self.store = None

    def test_it_returns_last_result(self):
        with self.store.bind.begin() as conn:
            conn.execute(schema.results.insert(), [
                { 'draw': 100, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'EM', 'mark_number': 1 },
                { 'draw': 101, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'AM', 'mark_number': 2 },
                { 'draw': 102, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'AN', 'mark_number': 3 },
                { 'draw': 103, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'PM', 'mark_number': 4 },
                { 'draw': 104, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'EM', 'mark_number': 5 },
                { 'draw': 105, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'AM', 'mark_number': 6 },
                { 'draw': 106, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'AN', 'mark_number': 7 },
                { 'draw': 107, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'PM', 'mark_number': 8 }
            ])

            last_result = conn.execute(select_last_result()).fetchone()

            self.assertEqual(last_result, (107, datetime.date(2000, 1, 2), 'PM', 8))

    def test_when_no_results(self):
        with self.store.bind.begin() as conn:
            last_result = conn.execute(select_last_result()).fetchone()

            self.assertIsNone(last_result)

    def test_when_draw_is_incorrect(self):
        with self.store.bind.begin() as conn:
            conn.execute(schema.results.insert(), [
                { 'draw': 100, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'EM', 'mark_number': 1 },
                { 'draw': 102, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'AN', 'mark_number': 3 },
                { 'draw': 103, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'PM', 'mark_number': 4 },
                { 'draw': 104, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'EM', 'mark_number': 5 },
                { 'draw': 105, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'AM', 'mark_number': 6 },
                { 'draw': 106, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'AN', 'mark_number': 7 },
                { 'draw': 107, 'date': datetime.date(2000, 1, 2), 'period_abbr': 'PM', 'mark_number': 8 },
                { 'draw': 201, 'date': datetime.date(2000, 1, 1), 'period_abbr': 'AM', 'mark_number': 2 },
            ])

            last_result = conn.execute(select_last_result()).fetchone()

            self.assertEqual(last_result, (107, datetime.date(2000, 1, 2), 'PM', 8))
