import argparse
import logging

from sqlalchemy import create_engine

from . import constants, db


logger = logging.getLogger(__name__)


def main(args=None):
    ns = argument_parser().parse_args(args)

    configure_logging(logging.INFO if ns.verbose else logging.ERROR)

    try:
        run(ns)
    except Exception:
        logger.exception('Sorry, an unexpected error occurred. Program terminated abnormally.')
        return 1

    return 0


def run(ns):
    engine = create_engine(ns.database_url)
    force_sync = True

    if ns.init:
        force_sync = False
        db.initialize(engine)

    if ns.csvfile:
        force_sync = False
        db.load(engine, ns.csvfile)

    if ns.sync or force_sync:
        db.sync(engine)


def argument_parser():
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description='Retrieve and store Play Whe results.')

    parser.add_argument('database_url', metavar='DATABASE_URL',
                        help='URL of the database to use. For e.g. '
                             'sqlite:////home/<username>/playwhe.db')

    parser.add_argument('-i', '--init', action='store_true',
                        help='initialize the database')

    parser.add_argument('-s', '--sync', action='store_true',
                        help='update the database with the latest results')

    parser.add_argument('-l', '--load', type=argparse.FileType('r', encoding='utf-8'),
                        metavar='CSV_FILE', dest='csvfile',
                        help='load results from the given CSV file into the database')

    parser.add_argument('-V', '--verbose', action='store_true',
                        help='verbose output')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + constants.VERSION)

    return parser


def configure_logging(level):
    logger = logging.getLogger('playwhe')
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
