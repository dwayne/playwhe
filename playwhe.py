#! /usr/bin/env python

"""A Python API and script for retrieving Play Whe results.

The library provides a Python interface for retrieving Play Whe results from
the National Lotteries Control Board (NLCB) website at http://www.nlcb.co.tt/.

The script uses the library to provide a tool for the retrieval of Play Whe
results.

"""

import datetime
import re
import sys

from operator import attrgetter
from urllib import urlencode
from urllib2 import urlopen, URLError

__version__ = "0.2"
__author__  = "Dwayne R. Crooks"
__email__   = "me@dwaynecrooks.com"

# Play Whe's birthday
start_date = datetime.date(1994, 7, 4) # July 4th, 1994

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

    def __init__(self, draw, date, time_of_day, number):
        """Create a result.

        draw        - a positive integer that uniquely identifies the result
        date        - a datetime.date object
        time_of_day - "AM" or "PM", indicating whether the draw was the
                      early (1:00 PM) draw or the late (6:30 PM) draw
        number      - a number between Mark.lowest and Mark.highest inclusive
        """
        if draw < 1:
            raise ValueError("draw is out of range")

        if not isinstance(date, datetime.date):
            raise TypeError("date is not a datetime.date object")

        if time_of_day not in ["AM", "PM"]:
            raise ValueError("time of day is invalid")

        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")

        self.draw = draw
        self.date = date
        self.time_of_day = time_of_day
        self.number = number

    def __repr__(self):
        return '%s(%d, %s, "%s", %d)' % \
            (self.__class__,
             self.draw,
             repr(self.date),
             self.time_of_day,
             self.number)

    def __str__(self):
        """Return a string representing the result in CSV format.

        For example, str(Result(1, playwhe.start_date, "AM", 15)) == "1,1994-07-04,AM,15".
        """
        return "%d,%s,%s,%d" % \
            (self.draw,
             self.date.isoformat(),
             self.time_of_day,
             self.number)

    def prettyprint(self):
        """Return a nicely formatted string representing the result."""
        return "Date:   %s-%s-%d\nTime:   %s\nDraw:   %d\nNumber: %d (%s)" % \
                (str(self.date.day).zfill(2),
                 month_abbr[self.date.month],
                 self.date.year,
                 self.time_of_day,
                 self.draw,
                 self.number,
                 Mark.get_name_of_number(self.number))

class PlayWheException(Exception):
    pass

class PlayWhe(object):

    def __init__(self,
                 host="nlcb.co.tt",
                 service="/search/pwq/countdateCash.php",
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
        """Return a list with the two most recent results.

        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, 1)

        try:
            results = self.results_for_month(date.year, date.month)
        except PlayWheException:
            raise PlayWheException("Unable to retrieve the results for the previous two drawings")

        while len(results) < 2:
            date = date - datetime.timedelta(1)
            date = datetime.date(date.year, date.month, 1)
            try:
                results = self.results_for_month(date.year, date.month) + results
            except PlayWheException:
                raise PlayWheException("Unable to retrieve the results for the previous two drawings")

        return results[-2:]

    def _parse_results(self, year, month, html):
        # html is a string of HTML containing Play Whe results of the form:
        #     <date>: Draw # <number> : <period>'s draw was <mark>
        pattern = r"(\d{2})-%s-%s: Draw # (\d+) : (AM|PM)'s draw  was (\d+)" % \
            (month_abbr[month], str(year % 100).zfill(2))

        results = []
        for r in re.findall(pattern, html):
            try:
                result = Result(int(r[1]),
                                datetime.date(year, month, int(r[0])),
                                r[2],
                                int(r[3]))
                results.append(result)
            except (ValueError, TypeError), e:
                print >> sys.stderr, 'IntegrityError: day(%d) draw(%d) time_of_day("%s") number(%d)' % (int(r[0]), int(r[1]), r[2], int(r[3]))

        return sorted(results, key=attrgetter("draw"))

if __name__ == "__main__":
    from optparse import OptionParser
    from sys import exit

    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog " + __version__,
                          description="A script for the retrieval and storage of Play Whe results.",
                          epilog="For more help or to report bugs, please contact %s at %s." % (__author__, __email__))
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

        network_connection_error = \
            "Sorry, unable to retrieve the results at this time.\n" + \
            "Please check your network connection and try again at a later time."

        if options.date:
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
                exit(1)
        else:
            try:
                display_results(PlayWhe().results())
            except PlayWheException:
                print network_connection_error
                exit(1)
    except KeyboardInterrupt:
        print
    except Exception:
        print "Sorry, an unknown error has occurred. Program terminated abnormally."
        exit(1)
