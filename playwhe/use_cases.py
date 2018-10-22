import numbers

from . import constants
from .db import query


class Mark:
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return 'Mark(%d, %s)' % (self.number, self.name)

    def __str__(self):
        return '%d (%s)' % (self.number, self.name)


def get_marks(conn):
    marks = conn.execute(query.select_marks()).fetchall()

    return [Mark(number, name) for number, name in marks]


def get_mark(conn, number):
    if not isinstance(number, numbers.Integral) or number < constants.MIN_NUMBER or number > constants.MAX_NUMBER:
        raise ValueError('number must be an integer between %d and %d inclusive: %r' % (constants.MIN_NUMBER, constants.MAX_NUMBER, number))

    number, name = conn.execute(query.select_mark(), number=number).fetchone()

    return Mark(number, name)


DEFAULT_LIMIT = 25
DEFAULT_PAGE = 1
DEFAULT_ORDER = 'DESC'

ORDERS = ('ASC', 'DESC')


def get_results(conn, **kwargs):
    year = None
    if 'year' in kwargs:
        if kwargs['year'] is None or (isinstance(kwargs['year'], numbers.Integral) and kwargs['year'] >= constants.MIN_YEAR):
            year = kwargs['year']
        else:
            raise ValueError('year must be an integer greater than or equal to %d: %r' % (constants.MIN_YEAR, kwargs['year']))

    month = None
    if 'month' in kwargs:
        if kwargs['month'] is None or (isinstance(kwargs['month'], numbers.Integral) and kwargs['month'] >= 1 and kwargs['month'] <= 12):
            month = kwargs['month']
        else:
            raise ValueError('month must be an integer between 1 and 12 inclusive: %r' % kwargs['month'])

    day = None
    if 'day' in kwargs:
        if kwargs['day'] is None or (isinstance(kwargs['day'], numbers.Integral) and kwargs['day'] >= 1 and kwargs['day'] <= 31):
            day = kwargs['day']
        else:
            raise ValueError('day must be an integer between 1 and 31 inclusive: %r' % kwargs['day'])

    draw = None
    if 'draw' in kwargs:
        if kwargs['draw'] is None or (isinstance(kwargs['draw'], numbers.Integral) and kwargs['draw'] >= 1):
            draw = kwargs['draw']
        else:
            raise ValueError('draw must be an integer greater than or equal to 1: %r' % kwargs['draw'])

    period = None
    if 'period' in kwargs:
        if kwargs['period'] is None or (kwargs['period'] in constants.PERIODS):
            period = kwargs['period']
        else:
            raise ValueError('period must be one of %s: %r' % (', '.join(constants.PERIODS), kwargs['period']))

    number = None
    if 'number' in kwargs:
        if kwargs['number'] is None or (isinstance(kwargs['number'], numbers.Integral) and kwargs['number'] >= constants.MIN_NUMBER and kwargs['number'] <= constants.MAX_NUMBER):
            number = kwargs['number']
        else:
            raise ValueError('number must be an integer between %d and %d inclusive: %r' % (constants.MIN_NUMBER, constants.MAX_NUMBER, kwargs['number']))

    limit = DEFAULT_LIMIT
    if 'limit' in kwargs:
        if kwargs['limit'] is None:
            limit = DEFAULT_LIMIT
        elif isinstance(kwargs['limit'], numbers.Integral) and kwargs['limit'] >= 1 and kwargs['limit'] <= 100:
            limit = kwargs['limit']
        else:
            raise ValueError('limit must be an integer between 1 and 100 inclusive: %r' % kwargs['limit'])

    page = DEFAULT_PAGE
    if 'page' in kwargs:
        if kwargs['page'] is None:
            page = DEFAULT_PAGE
        elif isinstance(kwargs['page'], numbers.Integral) and kwargs['page'] >= 1:
            page = kwargs['page']
        else:
            raise ValueError('page must be an integer greater than or equal to 1: %r' % kwargs['page'])

    order = DEFAULT_ORDER
    if 'order' in kwargs:
        if kwargs['order'] is None:
            order = DEFAULT_ORDER
        elif kwargs['order'] in ORDERS:
            order = kwargs['order']
        else:
            raise ValueError('order must be one of %s: %r' % (', '.join(ORDERS), kwargs['order']))

    # At this point everyone is set appropriately.
    # TODO: Perform the query and return the results.


def get_results_by_week():
    pass


def get_mark_counts_by_date():
    pass


def get_mark_counts_by_weekday():
    pass


def get_last_draws_by_date():
    pass
