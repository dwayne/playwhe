import datetime
import unittest

from playwhe.db.result import Result


class ResultTestCase(unittest.TestCase):
    def test_when_valid(self):
        result = Result((1, 1994, 7, 4, 'AM', 15))

        self.assertTrue(result.is_valid())
        self.assertEqual(result.full_error_message(), '')
        self.assertEqual(result.values(), {
            'draw': 1,
            'date': datetime.date(1994, 7, 4),
            'period': 'AM',
            'number': 15
        })

    def test_when_draw_is_invalid(self):
        result = Result((0, 1994, 7, 4, 'AM', 15))

        self.assertFalse(result.is_valid())
        self.assertEqual(result.full_error_message(), 'draw must be greater than or equal to 1, given 0')

    def test_when_date_is_invalid(self):
        result = Result((1, 1994, 0, 4, 'AM', 15))

        self.assertFalse(result.is_valid())
        self.assertEqual(result.full_error_message(), 'year, month and day must represent a valid date, given 1994, 0 and 4')

    def test_when_number_is_invalid(self):
        result = Result((1, 1994, 7, 4, 'AM', 37))

        self.assertFalse(result.is_valid())
        self.assertEqual(result.full_error_message(), 'number must be between 1 and 36 inclusive, given 37')

    def test_when_period_is_invalid(self):
        result = Result((1, 1994, 7, 4, 'XM', 15))

        self.assertFalse(result.is_valid())
        self.assertEqual(result.full_error_message(), 'period must be one of EM, AM, AN, PM, given XM')

    def test_when_multiple_values_are_invalid(self):
        result = Result((0, 1994, 7, 4, 'XM', 15))

        self.assertFalse(result.is_valid())
        self.assertEqual(result.full_error_message(), '\n'.join([
            'draw must be greater than or equal to 1, given 0',
            'period must be one of EM, AM, AN, PM, given XM'
        ]))
