import unittest

from playwhe.client.parser import parse
from playwhe.common import Params, Result

from . import fake


class ParseTestCase(unittest.TestCase):
    def test_it_parses(self):
        cases = [
            { 'params': Params(1994, 7),
              'count': 48,
              'first': Result(1, 1994, 7, 4, 'AM', 15),
              'last': Result(48, 1994, 7, 30, 'PM', 28)
            },
            { 'params': Params(2015, 7),
              'count': 100,
              'first': Result(14018, 2015, 7, 1, 'EM', 24),
              'last': Result(14117, 2015, 7, 31, 'PM', 25)
            },
            { 'params': Params(2011, 11),
              'count': 59,
              'first': Result(10652, 2011, 11, 1, 'PM', 14),
              'last': Result(10711, 2011, 11, 30, 'PM', 14)
            }
        ]

        for case in cases:
            params = case['params']
            html = fake.response(params)

            results = parse(html, params)

            with self.subTest(params=params):
                self.assertEqual(len(results), case['count'])
                self.assertEqual(results[0], case['first'])
                self.assertEqual(results[-1], case['last'])
