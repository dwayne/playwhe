import unittest
from unittest.mock import Mock

from playwhe.scraper import scrape, to_mmm, to_yy

from .util import mock_response


class ScrapeFromMockServerTestCase(unittest.TestCase):
    def test_it_works(self):
        post = Mock(name='post')
        post.return_value = Mock(name='response', status_code=200, text=mock_response('94', 'Jul'))

        raw_results = scrape(1994, 7, post=post)

        self.assertEqual(len(raw_results), 48)


@unittest.skip('it connects to a real server')
class ScrapeFromRealServerTestCase(unittest.TestCase):
    def test_it_works(self):
        raw_results = scrape(1994, 7)

        self.assertEqual(len(raw_results), 48)


class YearConversionTestCase(unittest.TestCase):
    def test_it_returns_last_2_digits_of_year(self):
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
    def test_it_returns_first_3_letters_of_month(self):
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
