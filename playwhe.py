"""A Python API for retrieving Play Whe results.

This library provides a pure Python interface for retrieving Play Whe
results from the National Lotteries Control Board (NLCB) website
at http://www.nlcb.co.tt/.

"""

import datetime, re
from operator import attrgetter
from urllib import urlencode
from urllib2 import urlopen, URLError

# the date of the first Play Whe draw
FIRST_DRAW = datetime.date(1994, 7, 4) # July 4th, 1994

LOWEST_MARK  = 1    # the lowest Play Whe mark
HIGHEST_MARK = 36   # the highest Play Whe mark

# associate marks with their standard names
_name_of_mark = {
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

def name_of_mark(mark):
    """Return the standard name of the given mark."""
    if mark < LOWEST_MARK or mark > HIGHEST_MARK:
        raise ValueError("mark is out of range")
    
    return _name_of_mark[mark]

class Draw:
    """A single Play Whe draw.
    
    """
    
    def __init__(self, number, date, time_of_day, mark):
        """Create a single Play Whe draw.
        
        number      - a positive integer that uniquely identifies the draw
        date        - the date of the draw
        time_of_day - "AM" or "PM", used to indicate whether the draw
                      was the early (1:00 PM) draw or the late (6:30 PM) draw
        mark        - the mark that played (LOWEST_MARK <= mark <= HIGHEST_MARK)
        """
        if number < 1:
            raise ValueError("number is out of range")
        
        if time_of_day not in ["AM", "PM"]:
            raise ValueError("unknown time of day")
        
        if mark < LOWEST_MARK or mark > HIGHEST_MARK:
            raise ValueError("mark is out of range")
        
        self.number = number
        self.date = date
        self.time_of_day = time_of_day
        self.mark = mark
    
    def __repr__(self):
        return '%s(%d, %s, "%s", %d)' % \
            (self.__class__,
             self.number, repr(self.date), self.time_of_day, self.mark)
    
    def __str__(self):
        """Return a string representing the draw in CSV format.
        
        For example, str(Draw(1, FIRST_DRAW, "AM", 15)) == "1,1994-07-04,AM,15".
        """
        return "%d,%s,%s,%d" % \
            (self.number, self.date.isoformat(), self.time_of_day, self.mark)

# the abbreviated months of the year
_month_abbr = ["",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

class PlayWheException(Exception):
    pass

class PlayWhe:
    
    def __init__(self,
                 host="nlcb.co.tt",
                 service="/search/pwq/countdateCash.php",
                 timeout=15):
        self._host = host
        self._service = service
        self._timeout = timeout
    
    def results_for_month(self, year, month):
        """Return a list of results for each day in the given month and year.
        
        The results are ordered in increasing order of the draw number.
        """
        if year == FIRST_DRAW.year and month == FIRST_DRAW.month:
            date = FIRST_DRAW
        else:
            date = datetime.date(year, month, 1)
    
        if date < FIRST_DRAW or date > datetime.date.today():
            return []
    
        params = urlencode({
            "year" : str(year % 100).zfill(2),
            "month": _month_abbr[month]
        })
    
        try:
            f = urlopen("http://" + self._host + self._service,
                        params, self._timeout)
            data = f.read()
            f.close()
        except URLError, AttributeError:
            raise PlayWheException("unable to retrieve results")
    
        return self._parse_results(year, month, data)
    
    def results_for_day(self, year, month, day):
        """Return a list of results for the given day.
        
        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date(year, month, day)
        draws = self.results_for_month(year, month)
        return filter(lambda draw: draw.date == date, draws)
    
    def results(self):
        """Return a list with the previous two results.
        
        The results are ordered in increasing order of the draw number.
        """
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, 1)
        
        draws = self.results_for_month(date.year, date.month)
        while len(draws) < 2:
            date = date - datetime.timedelta(1)
            date = datetime.date(date.year, date.month, 1)
            draws = self.results_for_month(date.year, date.month) + draws
        
        return draws[-2:]
    
    def _parse_results(self, year, month, data):
        # data is a string of HTML containing Play Whe results of the form:
        #     <date>: Draw # <number> : <period>'s draw was <mark>
        pattern = r"(\d{2})-%s-%s: Draw # (\d+) : (AM|PM)'s draw  was (\d+)" % \
            (_month_abbr[month], str(year % 100).zfill(2))
        
        results = re.findall(pattern, data)
        
        draws = []
        for r in results:
            try:
                draw = Draw(int(r[1]),
                            datetime.date(year, month, int(r[0])),
                            r[2],
                            int(r[3]))
                draws.append(draw)
            except ValueError:
                # TODO: report/log invalid results
                pass
        
        return sorted(draws, key=attrgetter('number'))

if __name__ == "__main__":
    from sys import exit
    
    try:
        output = map(lambda d:
                        "Date: %s-%s-%d\nTime: %s\nDraw: %d\nMark: %d (%s)" % \
                            (str(d.date.day).zfill(2),
                             _month_abbr[d.date.month],
                             d.date.year,
                             d.time_of_day,
                             d.number,
                             d.mark,
                             name_of_mark(d.mark)),
                     reversed(PlayWhe().results()))
        print "\n\n".join(output)
    except PlayWheException:
        print "Sorry, unable to retrieve results at this time. Try again later."
        exit(1)
    except KeyboardInterrupt:
        pass
    except:
        print "An unknown error occurred."
        exit(1)
