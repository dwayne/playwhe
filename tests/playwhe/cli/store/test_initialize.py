import unittest

from sqlalchemy import bindparam, exists, select

from playwhe.cli.store import Store, schema
from playwhe.constants import MARKS, PERIODS


class InitializeTestCase(unittest.TestCase):
    def setUp(self):
        self.store = Store()

    def tearDown(self):
        self.store = None

    def test_it_creates_tables_and_seeds_marks_and_periods(self):
        self.store.initialize()

        # Ensure that all the tables were created
        for table in schema.metadata.tables.values():
            with self.subTest(table=table.name):
                self.assertTrue(table.exists(self.store.bind))

        # Ensure that the marks table was seeded
        NUMBER_EXITS_STMT = select([exists().where(schema.marks.c.number == bindparam('number'))])
        for number in MARKS.keys():
            with self.subTest(number=number):
                self.assertTrue(self.store.bind.execute(NUMBER_EXITS_STMT, number=number).scalar())

        # Ensure that the periods table was seeded
        PERIOD_EXISTS_STMT = select([exists().where(schema.periods.c.abbr == bindparam('abbr'))])
        for abbr in PERIODS.keys():
            with self.subTest(period=abbr):
                self.assertTrue(self.store.bind.execute(PERIOD_EXISTS_STMT, abbr=abbr).scalar())

    def test_it_is_idempotent(self):
        self.store.initialize()
        self.store.initialize()
