import logging

from sqlalchemy import case, create_engine, select

from . import schema
from .. import client
from ..common import Results, date_range
from ..constants import MARKS, PERIODS


logger = logging.getLogger(__name__)


class Store:
    def __init__(self, bind=None):
        if bind is None:
            self.bind = create_engine('sqlite:///:memory:')
        else:
            self.bind = bind

    def initialize(self):
        """Creates all the tables and then seeds the ones that need to be prepopulated.

        Currently only the marks and periods tables need to be prepopulated.
        """
        logger.info('Initialization started...')

        with self.bind.begin() as conn:
            logger.info('Creating the tables...')
            schema.metadata.create_all(conn)

            logger.info('Seeding the marks table...')
            conn.execute(
                schema.marks.insert().prefix_with('OR IGNORE'),
                [{ 'number': m.number, 'name': m.name } for m in MARKS.values()]
            )

            logger.info('Seeding the periods table...')
            conn.execute(
                schema.periods.insert().prefix_with('OR IGNORE'),
                [{ 'abbr': p.abbr, 'label': p.label, 'time_of_day': p.time_of_day } for p in PERIODS.values()]
            )

        logger.info('Initialization done!')

    def load(self, csvfile):
        """Inserts results from the given CSV file."""
        logger.info('Loading started...')

        logger.info('Reading the results from the CSV file...')
        results = Results.from_csvfile(csvfile)

        logger.info('Inserting the results...')
        insert(self.bind, results)

        logger.info('Loading done!')

    def update(self, fetch=client.fetch, today=None):
        """Updates results with the latest from the server."""
        kwargs = {}

        if today is not None:
            kwargs['today'] = today

        with self.bind.connect() as conn:
            last_result = conn.execute(select_last_result()).fetchone()

            if last_result is not None:
                kwargs['start_date'] = last_result.date
                kwargs['period'] = last_result.period_abbr

            try:
                if last_result is None:
                    logger.info('Update started...')
                else:
                    logger.info('Update resumed...')

                for year, month in date_range(**kwargs):
                    logger.info('Updating year={}, month={}...'.format(year, month))

                    insert(conn, fetch(year, month))

                    logger.info('Update for year={}, month={} done!'.format(year, month))
            except KeyboardInterrupt:
                logger.info('Update stopped!')
            else:
                logger.info('Update done!')


def insert(bind, results):
    if results:
        bind.execute(
            schema.results.insert().prefix_with('OR IGNORE'),
            [{ 'draw': r.draw, 'date': r.date, 'period_abbr': r.period, 'mark_number': r.number } for r in results]
        )

    if not results.all_valid():
        logger.error(results.full_error_messages())


PERIODS_DESC = {
    'EM': 3,
    'AM': 2,
    'AN': 1,
    'PM': 0
}


def select_last_result():
    return select([schema.results]). \
        order_by(schema.results.c.date.desc()). \
        order_by(case(PERIODS_DESC, value=schema.results.c.period_abbr)). \
        order_by(schema.results.c.draw.desc()). \
        limit(1)
