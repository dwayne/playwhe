import csv
import datetime
import logging

from ..constants import PERIODS, SPIRITS, START_DATE
from ..scraper import scrape

from .query import select_last_result
from .result import Result
from .schema import marks, metadata, results


logger = logging.getLogger(__name__)


def initialize(engine):
    """Create all the tables and add every mark."""

    with engine.begin() as conn:
        metadata.create_all(conn)

        values = [{ 'number': number, 'name': spirit } for number, spirit in SPIRITS.items()]
        conn.execute(marks.insert().prefix_with('OR IGNORE'), values)


def load(engine, csvfile):
    """Add the results from the given CSV file."""

    with engine.begin() as conn:
        insert(conn, map(to_raw_result, csv.reader(csvfile)))


def to_raw_result(line):
    l = line + ['', '', '', '']

    draw = to_int(l[0])
    year, month, day = (list(map(to_int, l[1].split('-'))) + [0, 0, 0])[:3]
    period = l[2]
    number = to_int(l[3])

    return (draw, year, month, day, period, number)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0


def sync(engine, scrape=scrape):
    """Update the results with the latest from the server."""

    try:
        with engine.connect() as conn:
            last_result = conn.execute(select_last_result()).fetchone()
            start_date, end_date = start_and_end_date(last_result)
            sync_from(conn, scrape, start_date, end_date)
    except KeyboardInterrupt:
        pass


def start_and_end_date(last_result, today=datetime.date.today):
    start_date = START_DATE

    if last_result:
        start_date = last_result['date']
        if last_result['period'] == PERIODS[-1]:
            start_date = start_date + datetime.timedelta(days=1)

    return (start_date, today())


def sync_from(conn, scrape, start_date, end_date):
    for year, month in date_range(start_date, end_date):
        logger.info('Syncing %s-%s...', year, str(month).zfill(2))

        with conn.begin():
            insert(conn, scrape(year, month))

        logger.info('Done syncing %s-%s', year, str(month).zfill(2))


def date_range(start_date, end_date):
    start_year = start_date.year
    end_year = end_date.year

    for year in range(start_year, end_year + 1):
        start_month = start_date.month if year == start_year else 1
        end_month = end_date.month if year == end_year else 12

        for month in range(start_month, end_month + 1):
            yield (year, month)


def insert(conn, raw_results):
    valid_results = []
    invalid_results = []

    for raw_result in raw_results:
        result = Result(raw_result)

        if result.is_valid():
            valid_results.append(result)
        else:
            invalid_results.append(result)

    conn.execute(results.insert().prefix_with('OR IGNORE'), [result.values() for result in valid_results])

    for result in invalid_results:
        logger.error('%s is invalid\n%s', result.raw_result, result.full_error_message())
