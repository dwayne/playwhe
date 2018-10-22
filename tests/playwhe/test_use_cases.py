import unittest

from sqlalchemy import create_engine

from playwhe import constants
from playwhe.db.tasks import initialize
from playwhe.use_cases import get_mark, get_marks


class GetMarksTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        initialize(self.engine)

    def test_it_returns_all_marks(self):
        with self.engine.begin() as conn:
            marks = get_marks(conn)

            self.assertEqual(len(marks), 36)
            for number, name in constants.SPIRITS.items():
                mark = marks[number-1]
                self.assertEqual(mark.number, number)
                self.assertEqual(mark.name, name)


class GetMarkTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        initialize(self.engine)

    def test_when_the_number_exists(self):
        with self.engine.begin() as conn:
            mark = get_mark(conn, 24)

            self.assertEqual(mark.number, 24)
            self.assertEqual(mark.name, 'queen')

    def test_when_the_number_does_not_exist(self):
        with self.engine.begin() as conn:
            bad_numbers = ['1', 0, 37, 4.5]
            for bad_number in bad_numbers:
                with self.subTest(number=bad_number):
                    with self.assertRaisesRegex(ValueError, 'number must be an integer between %d and %d inclusive: %r' % (1, 36, bad_number)):
                        get_mark(conn, bad_number)
