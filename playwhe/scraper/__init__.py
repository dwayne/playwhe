from .client import fetch
from .parser import parse


def scrape(year, month, url=None, timeout=None, post=None):
    """Fetch and parse the results for the given year and month."""

    kwargs = {}

    if url is not None:
        kwargs['url'] = url

    if timeout is not None:
        kwargs['timeout'] = timeout

    if post is not None:
        kwargs['post'] = post

    yy = to_yy(year)
    mmm = to_mmm(month)

    return parse(fetch(yy, mmm, **kwargs), year, month, yy, mmm)


def to_yy(year):
    """Returns the last 2 digits of the year."""
    return str(year % 100).zfill(2)


MONTH_ABBR = ['',
    'Jan', 'Feb', 'Mar',
    'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep',
    'Oct', 'Nov', 'Dec'
]


def to_mmm(month):
    """Returns the first 3 letters of the month.
    The first letter is capitalized.
    """
    return MONTH_ABBR[month]
