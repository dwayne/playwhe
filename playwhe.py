"""A Python API for retrieving Play Whe results.

This library provides a Python interface for retrieving Play Whe results from
the National Lotteries Control Board (NLCB) website at http://www.nlcb.co.tt/.

"""

import datetime
import re

from operator import attrgetter
from urllib import urlencode
from urllib2 import urlopen, URLError

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
        
        self.__number = number
        self.__name = name_of_mark[number]
    
    number = property(lambda self: self.__number)
    name = property(lambda self: self.__name)
    
    @staticmethod
    def get_name_of_number(number):
        """Return the standard name associated with the given number."""
        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")
        
        return Mark.name_of_number[number]
    
    def __repr__(self):
        return '%s(%d, "%s")' % (self.__class__, self.__mark, self.__name)
    
    def __str__(self):
        return "%d (%s)" % (self.__number, self.__name)

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
            raise ValueError("date is invalid")
        
        if time_of_day not in ["AM", "PM"]:
            raise ValueError("time of day is invalid")
        
        if number < Mark.lowest or number > Mark.highest:
            raise ValueError("number is out of range")
        
        self.__draw = draw
        self.__date = date
        self.__time_of_day = time_of_day
        self.__number = number
    
    draw = property(lambda self: self.__draw)
    date = property(lambda self: self.__date)
    time_of_day = property(lambda self: self.__time_of_day)
    number = property(lambda self: self.__number)
    
    def __repr__(self):
        return '%s(%d, %s, "%s", %d)' % \
            (self.__class__,
             self.__draw,
             repr(self.__date),
             self.__time_of_day,
             self.__number)
    
    def __str__(self):
        """Return a string representing the result in CSV format.
        
        For example, str(Result(1, playwhe.start_date, "AM", 15)) == "1,1994-07-04,AM,15".
        """
        return "%d,%s,%s,%d" % \
            (self.__draw,
             self.__date.isoformat(),
             self.__time_of_day,
             self.__number)
    
    def prettyprint(self):
        """Return a nicely formatted string representing the result."""
        return "Date:   %s-%s-%d\nTime:   %s\nDraw:   %d\nNumber: %d (%s)" % \
                (str(self.__date.day).zfill(2),
                 month_abbr[self.__date.month],
                 self.__date.year,
                 self.__time_of_day,
                 self.__draw,
                 self.__number,
                 Mark.get_name_of_number(self.__number))

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
        except URLError, AttributeError:
            raise PlayWheException("unable to retrieve results")
    
        return self._parse_results(year, month, html)
    
    def results_for_day(self, year, month, day):
        """Return a list of results for the given day.
        
        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date(year, month, day) # performs date validation
        results = self.results_for_month(year, month)
        return filter(lambda r: r.date == date, results)
    
    def results(self):
        """Return a list with the previous two results.
        
        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, 1)
        results = self.results_for_month(date.year, date.month)
        
        while len(results) < 2:
            date = date - datetime.timedelta(1)
            date = datetime.date(date.year, date.month, 1)
            results = self.results_for_month(date.year, date.month) + results
        
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
            except ValueError:
                # TODO: report/log invalid results
                pass
        
        return sorted(results, key=attrgetter('draw'))

if __name__ == "__main__":
    from sys import exit
    
    try:
        print "\n\n".join(map(lambda r: r.prettyprint(),
                          reversed(PlayWhe().results())))
    except PlayWheException:
        print "Sorry, unable to retrieve results at this time. Try again later."
        exit(1)
    except KeyboardInterrupt:
        pass
    except:
        print "Sorry, an unknown error has occurred."
        exit(1)
