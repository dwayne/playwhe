import os
import unittest

from unittest.mock import Mock

from requests import RequestException

from playwhe.client.fetcher import fetch
from playwhe.common import Params
from playwhe.errors import BadStatusCodeError, ServiceUnavailableError


class FetchFromMockServerTestCase(unittest.TestCase):
    def setUp(self):
        self.params = Params(1994, 7)
        self.post = Mock(name='post')

    def test_when_it_succeeds(self):
        self.post.return_value = Mock(name='response', status_code=200, text='HTML')

        self.assertEqual(fetch(self.params, post=self.post), 'HTML')

        self.post.assert_called_once()

    def test_when_it_fails_to_post(self):
        self.post.side_effect = RequestException()

        with self.assertRaises(ServiceUnavailableError):
            fetch(self.params, post=self.post)

    def test_when_not_200_response(self):
        for bad_status_code in [201, 300, 404, 500]:
            self.post.return_value = Mock(name='response', status_code=bad_status_code)

            with self.subTest(bad_status_code=bad_status_code):
                with self.assertRaisesRegex(BadStatusCodeError, str(bad_status_code)):
                    fetch(self.params, post=self.post)


@unittest.skipIf(os.environ.get('PLAYWHE_TESTS_USE_REAL_SERVER') is None, 'it connects to a real server')
class FetchFromRealServerTestCase(unittest.TestCase):
    def test_fetch(self):
        from . import fake

        cases = [
            Params(1994, 7),
            Params(2011, 11),
            Params(2015, 7)
        ]

        for params in cases:
            with self.subTest(params=params):
                self.assertEqual(fetch(params), fake.response(params))
