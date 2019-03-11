import os
import unittest

from unittest.mock import Mock

from playwhe import client
from playwhe.common import Params

from . import fake


class ScrapeFromMockServerTestCase(unittest.TestCase):
    def test_it_works(self):
        params = Params(1994, 7)
        post = Mock(name='post')
        post.return_value = Mock(name='response', status_code=200, text=fake.response(params))

        results = client.fetch(params.year, params.month, post=post)

        self.assertEqual(len(results), 48)
        self.assertEqual(len(results.invalid), 0)


@unittest.skipIf(os.environ.get('PLAYWHE_TESTS_USE_REAL_SERVER') is None, 'it connects to a real server')
class ScrapeFromRealServerTestCase(unittest.TestCase):
    def test_it_works(self):
        results = client.fetch(1994, 7)

        self.assertEqual(len(results), 48)
        self.assertEqual(len(results.invalid), 0)
