#! /usr/bin/env python

"""A Python API and script for retrieving and storing Play Whe results.

The library provides a Python interface for retrieving Play Whe results from
the National Lotteries Control Board (NLCB) website at http://www.nlcb.co.tt/.

The script uses the library to provide a tool for the retrieval and storage
of Play Whe results.

"""

import datetime
import re
import sys

from operator import attrgetter
from urllib import urlencode
from urllib2 import urlopen, URLError

__version__ = "0.5"
__author__  = "Dwayne R. Crooks"
__email__   = "me@dwaynecrooks.com"

# Play Whe's birthday
start_date = datetime.date(1994, 7, 4) # July 4th, 1994

# The date that Play Whe changed to having 3 draws per day
three_draws_date = datetime.date(2011, 11, 21) # November 21st, 2011

# the abbreviated months of the year
month_abbr = ["",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

class Mark(object):
    """A Play Whe mark."""

    lowest  = 1  # the lowest Play Whe mark
    highest = 36 # the highest Play Whe mark

    # associate the marks with their standard name
    name_of_number = {
        1: "centipede",
        2: "old lady",
        3: "carriage",
        4: "dead man",
        5: "parson man",
        6: "belly",
        7: "hog",
        8: "tiger",
        9: "cattle",
       10: "monkey",
       11: "corbeau",
       12: "king",
       13: "crapaud",
       14: "money",
       15: "sick woman",
       16: "jamette",
       17: "pigeon",
       18: "water boat",
       19: "horse",
       20: "dog",
       21: "mouth",
       22: "rat",
       23: "house",
       24: "queen",
       25: "morocoy",
       26: "fowl",
       27: "little snake",
       28: "red fish",
       29: "opium man",
       30: "house cat",
       31: "parson wife",
       32: "shrimps",
       33: "spider",
       34: "blind man",
       35: "big snake",
       36: "donkey"
    }

    def __init__(self, number):
        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")

        self.number = number
        self.name = Mark.name_of_number[number]

    @staticmethod
    def get_name_of_number(number):
        """Return the standard name associated with the given number."""
        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")

        return Mark.name_of_number[number]

    def __repr__(self):
        return '%s(%d, "%s")' % (self.__class__, self.number, self.name)

    def __str__(self):
        return "%d (%s)" % (self.number, self.name)

class Result(object):
    """A Play Whe result."""

    def __init__(self, draw, date, period, number):
        """Create a result.

        draw        - a positive integer that uniquely identifies the result
        date        - a datetime.date object
        period      - 1, 2 or 3, indicating whether the draw was the
                      1st (10:30 AM), 2nd (1:00 PM) or 3rd (6:30 PM) draw
        number      - a number between Mark.lowest and Mark.highest inclusive
        """
        if draw < 1:
            raise ValueError("draw is out of range")

        if not isinstance(date, datetime.date):
            raise TypeError("date is not a datetime.date object")

        if period not in [1, 2, 3]:
            raise ValueError("period is invalid")

        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")

        self.draw = draw
        self.date = date
        self.period = period
        self.number = number

    def __repr__(self):
        return '%s(%d, %s, %d, %d)' % \
            (self.__class__,
             self.draw,
             repr(self.date),
             self.period,
             self.number)

    def __str__(self):
        """Return a string representing the result in CSV format.

        For example, str(Result(1, playwhe.start_date, 1, 15)) == "1,1994-07-04,1,15".
        """
        return "%d,%s,%d,%d" % \
            (self.draw,
             self.date.isoformat(),
             self.period,
             self.number)

    def prettyprint(self):
        """Return a nicely formatted string representing the result."""
        return "Date:   %s-%s-%d\nDraw:   %d\nPeriod: %d\nNumber: %d (%s)" % \
                (str(self.date.day).zfill(2),
                 month_abbr[self.date.month],
                 self.date.year,
                 self.draw,
                 self.period,
                 self.number,
                 Mark.get_name_of_number(self.number))

class PlayWheException(Exception):
    pass

class PlayWhe(object):

    def __init__(self,
                 host="nlcb.co.tt",
                 service="/app/index.php/pwresults/playwhemonthsum",
                 timeout=15):
        self.host = host
        self.service = service
        self.timeout = timeout

    def results_for_month(self, year, month):
        """Return a list of results for each day in the given month and year.

        The results are ordered in increasing order of the draw number.
        """
        if year == start_date.year and month == start_date.month:
            date = start_date
        else:
            date = datetime.date(year, month, 1)

        if date < start_date or date > datetime.date.today():
            return []

        params = urlencode({
            "year" : str(year % 100).zfill(2),
            "month": month_abbr[month]
        })

        try:
            f = urlopen("http://" + self.host + self.service,
                        params,
                        self.timeout)
            html = f.read()
            f.close()
        except IOError, AttributeError:
            raise PlayWheException("Unable to retrieve the results for %d-%s" % \
                (year, str(month).zfill(2)))

        return self._parse_results(year, month, html)

    def results_for_day(self, year, month, day):
        """Return a list of results for the given day.

        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date(year, month, day) # performs date validation

        try:
            results = self.results_for_month(year, month)
        except PlayWheException:
            raise PlayWheException("Unable to retrieve the results for %d-%s-%s" % \
                (year, str(month).zfill(2), str(day).zfill(2)))

        return filter(lambda r: r.date == date, results)

    def results(self):
        """Return a list with the three most recent results.

        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, 1)

        try:
            results = self.results_for_month(date.year, date.month)
        except PlayWheException:
            raise PlayWheException("Unable to retrieve the results for the previous two drawings")

        while len(results) < 3:
            date = date - datetime.timedelta(1)
            date = datetime.date(date.year, date.month, 1)
            try:
                results = self.results_for_month(date.year, date.month) + results
            except PlayWheException:
                raise PlayWheException("Unable to retrieve the results for the previous two drawings")

        return results[-3:]

    def _parse_results(self, year, month, html):
        # html is a string of HTML containing Play Whe results of the form:
        #     <h2>
        #         <strong> Draw #: </strong>13721<br>
        #         <strong> Date: </strong>04-Mar-15<br>
        #         <strong> Mark Drawn: </strong>19<br>
        #         <strong> Drawn at: </strong>EM<br>
        #     </h2>
        # html is a string of HTML containing Play Whe results of the form:
        #     <date>: Draw # <number> : <period>'s draw was <mark>
        pattern = r"Draw #: </strong>(\d+).*? Date: </strong>(\d{1,2})-%s-%s.*? Mark Drawn: </strong>(\d+).*? Drawn at: </strong>(EM|AM|PM)" % \
            (month_abbr[month], str(year % 100).zfill(2))

        results = []
        for r in re.findall(pattern, html, re.IGNORECASE):
            try:
                result = Result(int(r[0]),
                                datetime.date(year, month, int(r[1])),
                                {'EM': 1, 'AM': 2, 'PM': 3}[r[3]],
                                int(r[2]))
                results.append(result)
            except (ValueError, TypeError), e:
                print >> sys.stderr, 'IntegrityError: day(%d) draw(%d) period("%s") number(%d)' % (int(r[1]), int(r[0]), r[3], int(r[2]))

        return sorted(results, key=attrgetter("draw"))

import sqlite3

def createdb(db_path):
    """Create and initialize a Play Whe database.

    db_path should be an absolute path to the database. For example,
    /home/<username>/playwhe.db.
    """
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error:
        raise PlayWheException("Sorry, unable to connect to the database at %s." % db_path)

    c = conn.cursor()

    # setup the initial tables and relationships
    c.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        number INTEGER PRIMARY KEY,
        name TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS results(
        draw INTEGER PRIMARY KEY,
        date TEXT,
        period INTEGER NOT NULL,
        number INTEGER NOT NULL REFERENCES marks(number)
    )""")

    # populate the marks table
    for number, name in Mark.name_of_number.iteritems():
        c.execute("INSERT OR IGNORE INTO marks VALUES(?,?)", (number, name))

    conn.commit()
    conn.close()

network_connection_error = \
    "Sorry, unable to retrieve the results at this time.\n" + \
    "Please check your network connection and try again at a later time."

def updatedb(db_path):
    """Update a Play Whe database with the latest results.

    db_path should be an absolute path to the database. For example,
    /home/<username>/playwhe.db.
    """
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error:
        raise PlayWheException("Sorry, unable to connect to the database at %s." % db_path)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM RESULTS ORDER BY DRAW DESC LIMIT 1")
    except sqlite3.Error:
        raise PlayWheException("Sorry, problems encountered accessing the database at %s." % db_path)

    last_result = c.fetchone()

    last = (start_date, "AM")
    if last_result:
        date = datetime.date(*map(int, last_result["date"].split('-')))
        if last_result["period"] == 1:
            last = (date, 2)
        elif last_result["period"] == 2:
            last = (date, 3)
        else:
            last = (date + datetime.timedelta(days=1), 1)
    last_date, last_time_of_day = last
    current_date = datetime.date.today()

    try:
        p = PlayWhe()
        for year in range(last_date.year, current_date.year + 1):

            start_month = last_date.month if year == last_date.year else 1
            end_month = current_date.month if year == current_date.year else 12

            for month in range(start_month, end_month + 1):
                print >> sys.stderr, "[%s] Fetching results for %s-%s..." % (datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p"), year, str(month).zfill(2)),

                try:
                    results = p.results_for_month(year, month)
                except PlayWheException:
                    raise PlayWheException(network_connection_error)
                for r in results:
                    conn.execute("INSERT OR IGNORE INTO results (draw, date, period, number) VALUES(?,?,?,?)", (r.draw, r.date.isoformat(), r.period, r.number))
                    conn.commit()

                print >> sys.stderr, "DONE!"
    finally:
        conn.close()

if __name__ == "__main__":
    from optparse import OptionParser
    import os.path

    parser = OptionParser(usage="usage: %prog [options]",
                          version=__version__,
                          description="A script for the retrieval and storage of Play Whe results.",
                          epilog="For more help or to report bugs, please contact %s at %s." % (__author__, __email__))
    parser.add_option("-c", "--createdb", dest="createdb_path", metavar="PATH",
                      help="create and initialize a Play Whe database. PATH must "
                           "be a path to the database you want to setup. For "
                           "example, /home/<username>/playwhe.db")
    parser.add_option("-u", "--updatedb", dest="updatedb_path", metavar="PATH",
                      help="update a Play Whe database with the latest results. "
                           "PATH must be a path to the database you want to "
                           "update. For example, /home/<username>/playwhe.db")
    parser.add_option("-d", "--date",
                      help="display all the results for DATE. DATE must take "
                           "one of the formats: yyyy-mm or yyyy-mm-dd. If DATE "
                           "has the format yyyy-mm then all the results for "
                           "the month in that year are displayed. Otherwise, "
                           "DATE has the format yyyy-mm-dd, and all the "
                           "results for that day are displayed")
    parser.add_option("-p", "--prettyprint",
                      action="store_true", default=False,
                      help="display results in a nice human readable format")

    (options, args) = parser.parse_args()

    try:
        def display_results(results):
            if results:
                if options.prettyprint:
                    print "\n\n".join(map(lambda r: r.prettyprint(), reversed(results)))
                else:
                    print "\n".join(map(str, reversed(results)))
            else:
                print "No results found."

        if options.createdb_path:
            createdb(os.path.abspath(options.createdb_path))
        elif options.updatedb_path:
            print "Press Ctrl-C to safely exit at anytime."
            print

            updatedb(os.path.abspath(options.updatedb_path))
        elif options.date:
            def results_for(year, month, day=None):
                if day is not None:
                    return PlayWhe().results_for_day(year, month, day)
                return PlayWhe().results_for_month(year, month)

            try:
                display_results(results_for(*map(int, options.date.split("-"))))
            except ValueError, TypeError:
                parser.error('Must be a valid date in the format "yyyy-mm" or "yyyy-mm-dd"')
            except PlayWheException:
                print network_connection_error
                sys.exit(1)
        else:
            try:
                display_results(PlayWhe().results())
            except PlayWheException:
                print network_connection_error
                sys.exit(1)
    except PlayWheException, e:
        print e
        sys.exit(1)
    except KeyboardInterrupt:
        print
    except Exception:
        print "Sorry, an unknown error has occurred. Program terminated abnormally."
        sys.exit(1)
