import logging


# Turn off logging by default
logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging


# The Public API
from .client import fetch
from .common import date_range
from .constants import \
    __version__, \
    FOUR_DRAWS_DATE, START_DATE, THREE_DRAWS_DATE, \
    MAX_YEAR, MIN_YEAR, \
    MAX_NUMBER, MIN_NUMBER, \
    AM, AN, EM, PM, PERIODS_ABBR, PERIODS, \
    MARKS
from .errors import \
    BadStatusCodeError, FetchError, PlayWheError, ServiceUnavailableError
