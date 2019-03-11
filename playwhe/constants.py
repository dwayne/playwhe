import datetime

from collections import namedtuple


__version__ = '0.8.0-alpha.2'


# Play Whe's birthday
START_DATE = datetime.date(1994, 7, 4) # July 4th, 1994


# The date that Play Whe changed to having 3 draws per day
THREE_DRAWS_DATE = datetime.date(2011, 11, 21) # November 21st, 2011


# The date that Play Whe changed to having 4 draws per day
FOUR_DRAWS_DATE = datetime.date(2015, 7, 6) # July 6th, 2015


# The year that Play Whe started
MIN_YEAR = 1994


# A reasonable upper bound for Play Whe years
MAX_YEAR = 2093


# The smallest Play Whe number
MIN_NUMBER = 1


# The largest Play Whe number
MAX_NUMBER = 36


# The abbreviations given to the times of day that Play Whe is played
EM = 'EM'
AM = 'AM'
AN = 'AN'
PM = 'PM'
PERIODS_ABBR = (EM, AM, AN, PM)


Period = namedtuple('Period', ['abbr', 'label', 'time_of_day'])


PERIODS = {
    EM: Period(EM, '10:30am', 10 * 3600 + 30 * 60),
    AM: Period(AM, '1:00pm', 13 * 3600),
    AN: Period(AN, '4:00pm', 16 * 3600),
    PM: Period(PM, '6:30pm', 18 * 3600 + 30 * 60)
}


Mark = namedtuple('Mark', ['number', 'name'])


MARKS = {
    1: Mark(1, 'centipede'),
    2: Mark(2, 'old lady'),
    3: Mark(3, 'carriage'),
    4: Mark(4, 'dead man'),
    5: Mark(5, 'parson man'),
    6: Mark(6, 'belly'),
    7: Mark(7, 'hog'),
    8: Mark(8, 'tiger'),
    9: Mark(9, 'cattle'),
   10: Mark(10, 'monkey'),
   11: Mark(11, 'corbeau'),
   12: Mark(12, 'king'),
   13: Mark(13, 'crapaud'),
   14: Mark(14, 'money'),
   15: Mark(15, 'sick woman'),
   16: Mark(16, 'jamette'),
   17: Mark(17, 'pigeon'),
   18: Mark(18, 'water boat'),
   19: Mark(19, 'horse'),
   20: Mark(20, 'dog'),
   21: Mark(21, 'mouth'),
   22: Mark(22, 'rat'),
   23: Mark(23, 'house'),
   24: Mark(24, 'queen'),
   25: Mark(25, 'morocoy'),
   26: Mark(26, 'fowl'),
   27: Mark(27, 'little snake'),
   28: Mark(28, 'red fish'),
   29: Mark(29, 'opium man'),
   30: Mark(30, 'house cat'),
   31: Mark(31, 'parson wife'),
   32: Mark(32, 'shrimps'),
   33: Mark(33, 'spider'),
   34: Mark(34, 'blind man'),
   35: Mark(35, 'big snake'),
   36: Mark(36, 'donkey')
}
