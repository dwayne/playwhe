import datetime
import io
import unittest

from playwhe.common import Params, Result, Results, Settings
from playwhe.common import date_range, to_mmm, to_yy
from playwhe.constants import MIN_YEAR, MAX_YEAR


class YearConversionTestCase(unittest.TestCase):
    def test_it_returns_last_2_digits_of_year_zero_padded(self):
        cases = [
            (1994, '94'),
            (2000, '00'),
            (2009, '09'),
            (2018, '18')
        ]

        for year, yy in cases:
            with self.subTest(year=year):
                self.assertEqual(to_yy(year), yy)


class MonthConversionTestCase(unittest.TestCase):
    def test_it_returns_first_3_letters_of_month_with_first_letter_capitalized(self):
        cases = [
            (1, 'Jan'),
            (2, 'Feb'),
            (3, 'Mar'),
            (4, 'Apr'),
            (5, 'May'),
            (6, 'Jun'),
            (7, 'Jul'),
            (8, 'Aug'),
            (9, 'Sep'),
            (10, 'Oct'),
            (11, 'Nov'),
            (12, 'Dec')
        ]

        for month, mmm in cases:
            with self.subTest(month=month):
                self.assertEqual(to_mmm(month), mmm)


class ParamsTestCase(unittest.TestCase):
    def test_when_year_and_month_are_valid(self):
        params = Params(1999, 1)

        self.assertEqual(params.year, 1999)
        self.assertEqual(params.yy, '99')
        self.assertEqual(params.month, 1)
        self.assertEqual(params.mmm, 'Jan')

    def test_when_year_is_invalid(self):
        invalid_years = [MIN_YEAR-1, MAX_YEAR+1]

        for invalid_year in invalid_years:
            with self.subTest(year=invalid_year):
                with self.assertRaisesRegex(ValueError, 'year={}'.format(invalid_year)):
                    Params(invalid_year, 1)

    def test_when_month_is_invalid(self):
        invalid_months = [0, 13]

        for invalid_month in invalid_months:
            with self.subTest(month=invalid_month):
                with self.assertRaisesRegex(ValueError, 'month={}'.format(invalid_month)):
                    Params(MIN_YEAR, invalid_month)


class SettingsTestCase(unittest.TestCase):
    def test_defaults(self):
        settings = Settings()

        self.assertEqual(settings.timeout, Settings.DEFAULT_TIMEOUT)
        self.assertEqual(settings.url, Settings.DEFAULT_URL)


class ResultTestCase(unittest.TestCase):
    def test_when_valid(self):
        result = Result(1, 1994, 7, 4, 'AM', 15)

        self.assertTrue(result.is_valid())
        self.assertEqual(result.draw, 1)
        self.assertEqual(result.date, datetime.date(1994, 7, 4))
        self.assertEqual(result.period, 'AM')
        self.assertEqual(result.number, 15)

    def test_when_draw_is_invalid(self):
        result = Result(0, 1994, 7, 4, 'AM', 15)

        self.assertFalse(result.is_valid())
        self.assertRegex(result.full_error_message(), 'draw must be a positive integer: draw=0')

    def test_when_date_is_invalid(self):
        result = Result(1, 1994, 0, 4, 'AM', 15)

        self.assertFalse(result.is_valid())
        self.assertRegex(result.full_error_message(), 'year, month and day must represent a valid date: year=1994, month=0, day=4')

    def test_when_number_is_invalid(self):
        result = Result(1, 1994, 7, 4, 'AM', 37)

        self.assertFalse(result.is_valid())
        self.assertRegex(result.full_error_message(), 'number must be an integer between 1 and 36 inclusive: number=37')

    def test_when_period_is_invalid(self):
        result = Result(1, 1994, 7, 4, 'XM', 15)

        self.assertFalse(result.is_valid())
        self.assertRegex(result.full_error_message(), 'period must be one of EM, AM, AN, PM: period=\'XM\'')

    def test_when_multiple_values_are_invalid(self):
        result = Result(0, 1994, 7, 4, 'XM', 15)

        self.assertFalse(result.is_valid())
        self.assertRegex(result.full_error_message(), 'draw must be a positive integer: draw=0')
        self.assertRegex(result.full_error_message(), 'period must be one of EM, AM, AN, PM: period=\'XM\'')


class ResultFromCSVLineTestCase(unittest.TestCase):
    def test_when_valid_string(self):
        result = Result.from_csvline('1,1994-07-04,AM,15')

        self.assertTrue(result.is_valid())
        self.assertEqual(result.draw, 1)
        self.assertEqual(result.date, datetime.date(1994, 7, 4))
        self.assertEqual(result.period, 'AM')
        self.assertEqual(result.number, 15)

    def test_when_valid_list_of_strings(self):
        result = Result.from_csvline(['1', '1994-07-04', 'AM', '15'])

        self.assertTrue(result.is_valid())
        self.assertEqual(result.draw, 1)
        self.assertEqual(result.date, datetime.date(1994, 7, 4))
        self.assertEqual(result.period, 'AM')
        self.assertEqual(result.number, 15)

    def test_when_invalid(self):
        cases = [
            None,
            0,
            '',
            '1',
            '1,1994',
            '1,1994-07',
            '1,1994-07-04',
            '1,1994-07-04,AM',
            [],
            ['1'],
            ['1', '1994'],
            ['1', '1994-07'],
            ['1', '1994-07-04'],
            ['1', '1994-07-04', 'AM'],
            [1],
            ['1', None]
        ]

        for csvline in cases:
            with self.subTest(csvline=csvline):
                self.assertFalse(Result.from_csvline(csvline).is_valid())


class ResultEqualityTestCase(unittest.TestCase):
    def test_when_both_valid(self):
        result1 = Result(1, 1994, 7, 4, 'AM', 15)
        result2 = Result(1, 1994, 7, 4, 'AM', 15)

        self.assertTrue(result1.is_valid())
        self.assertTrue(result2.is_valid())

        self.assertEqual(result1, result2)
        self.assertEqual(result2, result1)

    def test_when_one_invalid(self):
        result1 = Result(1, 1994, 7, 4, 'AM', 15)
        result2 = Result(0, 1994, 7, 4, 'AM', 15)

        self.assertTrue(result1.is_valid())
        self.assertFalse(result2.is_valid())

        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result1)

    def test_when_both_invalid(self):
        result1 = Result(1, 1994, 7, 4, 'AM', 0)
        result2 = Result(0, 1994, 7, 4, 'AM', 15)

        self.assertFalse(result1.is_valid())
        self.assertFalse(result2.is_valid())

        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result1)


class ResultsFromCSVFileTestCase(unittest.TestCase):
    def test_it_works(self):
        cases = [
            ('', 0, 0),
            (' ', 0, 0),
            ('\n', 0, 0),
            ('  \n\n\n\n    \n  ', 0, 0),
            ('1,1994-07-04,AM,15', 1, 0),
            ('1,1994-07-04,AM,15\n2,1994-07-04,PM,11\n3,1994-07-05,AM,36\n4,1994-07-05,PM,31\n', 4, 0),
            ('\n1\n\n1,1994\n1,1994-07-04,AM,15', 1, 2),
            ('apple\nbat\ncat\ndog', 0, 4)
        ]

        for contents, num_valid, num_invalid in cases:
            with self.subTest(contents=contents):
                csvfile = io.StringIO(contents)
                results = Results.from_csvfile(csvfile)

                self.assertEqual(len(results), num_valid)
                self.assertEqual(len(results.invalid), num_invalid)

    def test_lineno_and_line_tracking(self):
        csvfile = io.StringIO('1,1994-07-04,AM,15\nbat \n3,1994-07-05,AM,36\n dog')
        results = Results.from_csvfile(csvfile)

        self.assertEqual(len(results), 2)
        self.assertEqual(len(results.invalid), 2)

        self.assertEqual(results.invalid[0].lineno, 2)
        self.assertEqual(results.invalid[0].line, 'bat ')

        self.assertEqual(results.invalid[1].lineno, 4)
        self.assertEqual(results.invalid[1].line, ' dog')

    def test_full_error_messages(self):
        csvfile = io.StringIO('1,1994-07-04,AM,15\n0,1994-07-04,AM,15\n1,1994-07-00,AM,15\n1,1994-07-04,XM,15\n1,1994-07-04,AM,37')
        results = Results.from_csvfile(csvfile)

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results.invalid), 4)

        self.assertEqual(results.full_error_messages(),
            "Line 2: '0,1994-07-04,AM,15'\n"
            "    draw must be a positive integer: draw='0'\n"
            "Line 3: '1,1994-07-00,AM,15'\n"
            "    year, month and day must represent a valid date: year='1994', month='07', day='00'\n"
            "Line 4: '1,1994-07-04,XM,15'\n"
            "    period must be one of EM, AM, AN, PM: period='XM'\n"
            "Line 5: '1,1994-07-04,AM,37'\n"
            "    number must be an integer between 1 and 36 inclusive: number='37'\n"
            "\n"
            "Total errors = 4"
        )


class DateRangeTestCase(unittest.TestCase):
    def test_when_there_is_no_start_date(self):
        output = list(date_range(today=lambda: datetime.date(1994, 10, 10)))

        self.assertEqual(output, [(1994, 7), (1994, 8), (1994, 9), (1994, 10)])

    def test_when_there_is_a_start_date_and_period_is_not_pm(self):
        output = list(date_range(start_date=datetime.date(1996, 1, 31), period='AN', today=lambda: datetime.date(1996, 3, 1)))

        self.assertEqual(output, [(1996, 1), (1996, 2), (1996, 3)])

    def test_when_there_is_a_start_date_and_period_is_pm(self):
        output = list(date_range(start_date=datetime.date(1996, 1, 31), period='PM', today=lambda: datetime.date(1996, 3, 1)))

        self.assertEqual(output, [(1996, 2), (1996, 3)])
