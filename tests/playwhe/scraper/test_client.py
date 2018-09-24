import unittest
from unittest.mock import Mock

from requests import RequestException

from playwhe.error import FetchError
from playwhe.scraper import client


class FetchFromMockServerTestCase(unittest.TestCase):
    def setUp(self):
        self.yy = '94'
        self.mmm = 'Jul'
        self.post = Mock(name='post')

    def test_when_it_succeeds(self):
        self.post.return_value = Mock(name='response', status_code=200, text='HTML')

        self.assertEqual(client.fetch(self.yy, self.mmm, post=self.post), 'HTML')

        self.post.assert_called_once()

    def test_when_it_fails_to_post(self):
        self.post.side_effect = RequestException()

        with self.assertRaisesRegex(FetchError, 'POST failed'):
            client.fetch(self.yy, self.mmm, post=self.post)

    def test_when_not_200_response(self):
        for bad_status_code in [201, 300, 404, 500]:
            self.post.return_value = Mock(name='response', status_code=bad_status_code)

            with self.subTest(bad_status_code=bad_status_code):
                with self.assertRaisesRegex(FetchError, 'Bad status code: %d' % bad_status_code):
                    client.fetch(self.yy, self.mmm, post=self.post)


@unittest.skip('it connects to a real server')
class FetchFromRealServerTestCase(unittest.TestCase):
    def test_fetch(self):
        from .util import mock_response

        cases = [
            ('94', 'Jul'),
            ('11', 'Nov'),
            ('15', 'Jul')
        ]

        for yy, mmm in cases:
            with self.subTest(yy=yy, mmm=mmm):
                self.assertEqual(client.fetch(yy, mmm), mock_response(yy, mmm))
