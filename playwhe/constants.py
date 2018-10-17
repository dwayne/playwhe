import datetime


PROGRAM_NAME = 'playwhe'


VERSION = '0.8.0-alpha.1'


# Play Whe's birthday
START_DATE = datetime.date(1994, 7, 4) # July 4th, 1994


# The date that Play Whe changed to having 3 draws per day
THREE_DRAWS_DATE = datetime.date(2011, 11, 21) # November 21st, 2011


# The date that Play Whe changed to having 4 draws per day
FOUR_DRAWS_DATE = datetime.date(2015, 7, 6) # July 6th, 2015


# The year that Play Whe started
MIN_YEAR = 1994


# A resonable upper bound for Play Whe years
MAX_YEAR = 2093


# The smallest Play Whe number
MIN_NUMBER = 1


# The largest Play Whe number
MAX_NUMBER = 36


# The names associated with each Play Whe number
SPIRITS = {
    1: 'centipede',
    2: 'old lady',
    3: 'carriage',
    4: 'dead man',
    5: 'parson man',
    6: 'belly',
    7: 'hog',
    8: 'tiger',
    9: 'cattle',
   10: 'monkey',
   11: 'corbeau',
   12: 'king',
   13: 'crapaud',
   14: 'money',
   15: 'sick woman',
   16: 'jamette',
   17: 'pigeon',
   18: 'water boat',
   19: 'horse',
   20: 'dog',
   21: 'mouth',
   22: 'rat',
   23: 'house',
   24: 'queen',
   25: 'morocoy',
   26: 'fowl',
   27: 'little snake',
   28: 'red fish',
   29: 'opium man',
   30: 'house cat',
   31: 'parson wife',
   32: 'shrimps',
   33: 'spider',
   34: 'blind man',
   35: 'big snake',
   36: 'donkey'
}


# The names given to the times of day that Play Whe is played
PERIODS = ('EM', 'AM', 'AN', 'PM')


# The times of day that Play Whe is played
TIMES_OF_DAY = {
    'EM': (10, 30), # 10:30 AM
    'AM': (13, 0),  #  1:00 PM
    'AN': (16, 0),  #  4:00 PM
    'PM': (18, 30)  #  6:30 PM
}
