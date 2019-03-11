import csv
import datetime

from .constants import MAX_NUMBER, MIN_NUMBER, \
    MAX_YEAR, MIN_YEAR, \
    PERIODS_ABBR, \
    START_DATE


class Params:
    def __init__(self, year, month):
        if year >= MIN_YEAR and year <= MAX_YEAR:
            self.year = year
        else:
            raise ValueError('year must be between {} and {} inclusive: year={!r}'.format(MIN_YEAR, MAX_YEAR, year))

        if month >= 1 and month <= 12:
            self.month = month
        else:
            raise ValueError('month must be between 1 and 12 inclusive: month={!r}'.format(month))

        self.yy = to_yy(year)
        self.mmm = to_mmm(month)

    def __repr__(self):
        return '{}(year={!r}, yy={!r}, month={!r}, mmm={!r})'.format(self.__class__.__name__, self.year, self.yy, self.month, self.mmm)


def to_yy(year):
    """Returns the last 2 digits of the year."""
    return str(year % 100).zfill(2)


MONTHS_ABBR = ['',
    'Jan', 'Feb', 'Mar',
    'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep',
    'Oct', 'Nov', 'Dec'
]


def to_mmm(month):
    """Returns the first 3 letters of the month.

    The first letter is capitalized.
    """
    return MONTHS_ABBR[month]


class Settings:
    DEFAULT_TIMEOUT = 5
    DEFAULT_URL = 'http://nlcb.co.tt/app/index.php/pwresults/playwhemonthsum'

    def __init__(self, timeout=DEFAULT_TIMEOUT, url=DEFAULT_URL):
        self.timeout = timeout
        self.url = url

    def __repr__(self):
        return '{}(timeout={!r}, url={!r})'.format(self.__class__.__name__, self.timeout, self.url)


class Result:
    @classmethod
    def from_csvline(cls, csvline, delimiter=','):
        if isinstance(csvline, str):
            csvline = csvline.split(delimiter)
        else:
            try:
                csvline = list(map(str, csvline))
            except:
                csvline = []

        line = csvline + ['', '', '', '']
        draw = line[0]
        year, month, day = (line[1].split('-') + ['', '', ''])[:3]
        period = line[2]
        number = line[3]

        return cls(draw, year, month, day, period, number)

    def __init__(self, draw, year, month, day, period, number):
        original_args = {
            'draw': draw,
            'year': year,
            'month': month,
            'day': day,
            'period': period,
            'number': number
        }

        self.errors = errors = []
        self.draw = None
        self.date = None
        self.period = None
        self.number = None

        # Clean and validate draw
        draw = _parse_int(draw)
        if draw < 1:
            errors.append('draw must be a positive integer: draw={!r}'.format(original_args['draw']))
        else:
            self.draw = draw

        # Clean and validate year, month, day
        year = _parse_int(year)
        month = _parse_int(month)
        day = _parse_int(day)
        try:
            self.date = datetime.date(year, month, day)
        except ValueError:
            errors.append('year, month and day must represent a valid date: year={!r}, month={!r}, day={!r}'.format(
                original_args['year'],
                original_args['month'],
                original_args['day'])
            )

        # Clean and validate period
        period = _parse_str(period).upper()
        if period not in PERIODS_ABBR:
            errors.append('period must be one of {}: period={!r}'.format(', '.join(PERIODS_ABBR), original_args['period']))
        else:
            self.period = period

        # Clean and validate number
        number = _parse_int(number)
        if number < MIN_NUMBER or number > MAX_NUMBER:
            errors.append('number must be an integer between {} and {} inclusive: number={!r}'.format(MIN_NUMBER, MAX_NUMBER, original_args['number']))
        else:
            self.number = number

    def __eq__(self, other):
        return type(other) is type(self) and \
            self.is_valid() and other.is_valid() and \
            self.draw == other.draw and \
            self.date == other.date and \
            self.period == other.period and \
            self.number == other.number

    def is_valid(self):
        return not self.errors

    def full_error_message(self):
        if hasattr(self, 'lineno'):
            header = 'Line {}: {!r}'.format(self.lineno, self.line)
        else:
            header = '{!r}'.format(self)

        reasons = '\n'.join(map(lambda e: '    ' + e, self.errors))

        return header + '\n' + reasons

    def __repr__(self):
        return '{}(draw={!r}, date={!r}, period={!r}, number={!r})'.format(self.__class__.__name__, self.draw, self.date, self.period, self.number)


def _parse_int(x):
    try:
        return int(x)
    except:
        return 0

def _parse_str(x):
    try:
        return str(x)
    except:
        return ''


class Results(list):
    @classmethod
    def from_csvfile(cls, csvfile):
        delimiter = csv.get_dialect('excel').delimiter

        results = []

        for lineno, line in enumerate(csv.reader(csvfile), start=1):
            contents = delimiter.join(line)

            if contents.strip():
                result = Result.from_csvline(line, delimiter=delimiter)

                # Track these values for error reporting purposes
                result.lineno = lineno
                result.line = contents

                results.append(result)

        return cls(results)

    def __init__(self, results):
        super().__init__()

        self.invalid = []

        for result in results:
            if result.is_valid():
                self.append(result)
            else:
                self.invalid.append(result)

    def all_valid(self):
        return not bool(self.invalid)

    def full_error_messages(self):
        messages = '\n'.join(map(lambda r: r.full_error_message(), self.invalid))
        footer = 'Total errors = {}'.format(len(self.invalid))

        return messages + '\n\n' + footer


def date_range(start_date=None, period=PERIODS_ABBR[0], today=datetime.date.today):
    if start_date is None:
        start_date = START_DATE
        period = PERIODS_ABBR[0]
    elif period == PERIODS_ABBR[-1]:
        start_date += datetime.timedelta(days=1)

    end_date = today()

    start_year = start_date.year
    end_year = end_date.year

    for year in range(start_year, end_year + 1):
        start_month = start_date.month if year == start_year else 1
        end_month = end_date.month if year == end_year else 12

        for month in range(start_month, end_month + 1):
            yield year, month
