import argparse
import logging
import shlex

from sqlalchemy import create_engine

from .store import Store
from ..constants import __version__


logger = logging.getLogger(__name__)


PARSER = argparse.ArgumentParser(
    prog='playwhe',
    description='Retrieve and store Play Whe results.'
)
PARSER.add_argument('database_url', metavar='DATABASE_URL',
    help='URL of the database to use. For e.g. sqlite:///$HOME/playwhe.db'
)
PARSER.add_argument('-i', '--init', action='store_true',
    help='initialize the database'
)
PARSER.add_argument('-u', '--update', action='store_true',
    help='update the database with the latest results'
)
PARSER.add_argument('-l', '--load',
    type=argparse.FileType('r', encoding='utf-8'),
    metavar='CSV_FILE', dest='csvfile',
    help='load the database with the results from the given CSV file'
)
PARSER.add_argument('-V', '--verbose', action='store_true',
    help='verbose output'
)
PARSER.add_argument('-v', '--version', action='version',
    version='%(prog)s ' + __version__
)


class CLI:
    def __init__(self, args=None):
        if args is not None:
            if isinstance(args, str):
                args = shlex.split(args)
            else:
                raise ValueError('args must be a string of command line arguments: {!r}'.format(args))

        self.namespace = PARSER.parse_args(args)
        self.configure()

    def __call__(self):
        try:
            self.run()
        except Exception:
            logger.exception('Program terminated abnormally.')
            return 1
        except KeyboardInterrupt:
            pass

        return 0

    def configure(self):
        self.configure_logging()
        self.configure_storage()

    def configure_logging(self):
        logger = logging.getLogger('playwhe')

        level = logging.INFO if self.namespace.verbose else logging.ERROR
        logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    def configure_storage(self):
        self.store = Store(create_engine(self.namespace.database_url))

    def run(self):
        force_update = True

        if self.namespace.init:
            force_update = False
            self.store.initialize()

        if self.namespace.csvfile:
            force_update = False
            self.store.load(self.namespace.csvfile)

        if self.namespace.update or force_update:
            self.store.update()


def main(args=None):
    return CLI(args)()
