import unittest

from playwhe.scraper.parser import parse, RawResult

from .util import mock_response


class ParseTestCase(unittest.TestCase):
    def test_it_parses(self):
        cases = [
            { 'year': 1994,
              'month': 7,
              'yy': '94',
              'mmm': 'Jul',
              'len': 48,
              'first': RawResult(1, 1994, 7, 4, 15, 'AM'),
              'last': RawResult(48, 1994, 7, 30, 28, 'PM')
            },
            { 'year': 2015,
              'month': 7,
              'yy': '15',
              'mmm': 'Jul',
              'len': 100,
              'first': RawResult(14018, 2015, 7, 1, 24, 'EM'),
              'last': RawResult(14117, 2015, 7, 31, 25, 'PM')
            },
            { 'year': 2011,
              'month': 11,
              'yy': '11',
              'mmm': 'Nov',
              'len': 59,
              'first': RawResult(10652, 2011, 11, 1, 14, 'PM'),
              'last': RawResult(10711, 2011, 11, 30, 14, 'PM')
            }
        ]

        for case in cases:
            year = case['year']
            month = case['month']
            yy = case['yy']
            mmm = case['mmm']
            html = mock_response(yy, mmm)

            raw_results = parse(html, year, month, yy, mmm)

            with self.subTest(year=year, month=month):
                self.assertEqual(len(raw_results), case['len'])
                self.assertEqual(raw_results[0], case['first'])
                self.assertEqual(raw_results[-1], case['last'])
