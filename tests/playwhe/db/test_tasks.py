import datetime
import io
import logging
import unittest

from sqlalchemy import bindparam, create_engine, exists, select

from playwhe.constants import SPIRITS, START_DATE
from playwhe.db import schema, tasks
from playwhe.db.tasks import date_range, insert, start_and_end_date, to_raw_result


class InitializeTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')

    def test_initialize(self):
        tasks.initialize(self.engine)

        # Ensure that all tables were created
        for table in schema.metadata.tables.values():
            with self.subTest(table=table.name):
                self.assertTrue(table.exists(self.engine))

        # Ensure that every mark was added
        NUMBER_EXITS_STMT = select([exists().where(schema.marks.c.number == bindparam('number'))])

        for number in SPIRITS.keys():
            with self.subTest(number=number):
                self.assertTrue(self.engine.execute(NUMBER_EXITS_STMT, number=number).scalar())

    def test_it_is_idempotent(self):
        tasks.initialize(self.engine)
        tasks.initialize(self.engine)


class LoadTestCase(unittest.TestCase):
    def test_load(self):
        engine = create_engine('sqlite:///:memory:')

        tasks.initialize(engine)

        csvfile = io.StringIO('1,1994-07-04,AM,15\n2,1994-07-04,PM,11\n3,1994-07-05,AM,36\n4,1994-07-05,PM,31\n')
        tasks.load(engine, csvfile)

        data = engine.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (1, datetime.date(1994, 7, 4), 'AM', 15))
        self.assertEqual(data[1], (2, datetime.date(1994, 7, 4), 'PM', 11))
        self.assertEqual(data[2], (3, datetime.date(1994, 7, 5), 'AM', 36))
        self.assertEqual(data[3], (4, datetime.date(1994, 7, 5), 'PM', 31))


class ToRawResultTestCase(unittest.TestCase):
    def test_to_raw_result(self):
        cases = [
            ([], (0, 0, 0, 0, '', 0)),
            (['1'], (1, 0, 0, 0, '', 0)),
            (['1', '1994'], (1, 1994, 0, 0, '', 0)),
            (['1', '1994-07'], (1, 1994, 7, 0, '', 0)),
            (['1', '1994-07-04'], (1, 1994, 7, 4, '', 0)),
            (['1', '1994-07-04', 'AM'], (1, 1994, 7, 4, 'AM', 0)),
            (['1', '1994-07-04', 'AM', 15], (1, 1994, 7, 4, 'AM', 15))
        ]

        for input, output in cases:
            with self.subTest(input=input):
                self.assertEqual(to_raw_result(input), output)


class StartAndEndDateTestCase(unittest.TestCase):
    def setUp(self):
        self.today = lambda: datetime.date(2000, 4, 19)
        self.last_result = { 'date': datetime.date(1996, 1, 1), 'period': 'AM' }

    def test_when_there_is_no_last_result(self):
        start_date, end_date = start_and_end_date(None, today=self.today)

        self.assertEqual(start_date, START_DATE)
        self.assertEqual(end_date, self.today())

    def test_when_there_is_a_last_result_and_period_is_not_pm(self):
        start_date, end_date = start_and_end_date(self.last_result, today=self.today)

        self.assertEqual(start_date, self.last_result['date'])
        self.assertEqual(end_date, self.today())

    def test_when_there_is_a_last_result_and_period_is_pm(self):
        self.last_result['period'] = 'PM'

        start_date, end_date = start_and_end_date(self.last_result, today=self.today)

        self.assertEqual(start_date, self.last_result['date'] + datetime.timedelta(days=1))
        self.assertEqual(end_date, self.today())


class DateRangeTestCase(unittest.TestCase):
    def test_date_range(self):
        start_date = datetime.date(1999, 10, 10)
        end_date = datetime.date(2001, 4, 2)

        output = [(year, month) for year, month in date_range(start_date, end_date)]

        self.assertEqual(output, [
            (1999, 10), (1999, 11), (1999, 12),
            (2000, 1), (2000, 2), (2000, 3), (2000, 4), (2000, 5), (2000, 6), (2000, 7), (2000, 8), (2000, 9), (2000, 10), (2000, 11), (2000, 12),
            (2001, 1), (2001, 2), (2001, 3), (2001, 4)
        ])


class InsertTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = engine = create_engine('sqlite:///:memory:')
        tasks.initialize(engine)

    def test_insert(self):
        raw_results = [
            (100, 1998, 4, 1, 'AM', 5),
            (101, 1998, 4, 1, 'PM', 17),
            (0, 1998, 4, 2, 'AM', 33)
        ]

        with self.engine.begin() as conn:
            with self.assertLogs('playwhe.db.tasks', level=logging.ERROR) as cm:
                insert(conn, raw_results)

                self.assertEqual(len(cm.output), 1)
                self.assertRegex(cm.output[0], r"\(0, 1998, 4, 2, 'AM', 33\) is invalid\ndraw must be greater than or equal to 1, given 0")

            data = conn.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

            self.assertEqual(len(data), 2)
            self.assertEqual(data[0], (100, datetime.date(1998, 4, 1), 'AM', 5))
            self.assertEqual(data[1], (101, datetime.date(1998, 4, 1), 'PM', 17))

    def test_it_ignores_previously_inserted_results(self):
        raw_results = [
            (10010, 2016, 7, 11, 'EM', 2),
            (10011, 2016, 7, 11, 'AM', 19)
        ]

        more_raw_results = [
            (10012, 2016, 7, 11, 'AN', 31),
            (10013, 2016, 7, 11, 'PM', 6)
        ]

        with self.engine.begin() as conn:
            insert(conn, raw_results)
            insert(conn, raw_results + more_raw_results)

            data = conn.execute(select([schema.results]).order_by(schema.results.c.draw)).fetchall()

            self.assertEqual(len(data), 4)
            self.assertEqual(data[0], (10010, datetime.date(2016, 7, 11), 'EM', 2))
            self.assertEqual(data[1], (10011, datetime.date(2016, 7, 11), 'AM', 19))
            self.assertEqual(data[2], (10012, datetime.date(2016, 7, 11), 'AN', 31))
            self.assertEqual(data[3], (10013, datetime.date(2016, 7, 11), 'PM', 6))
