import datetime

from ..constants import MAX_NUMBER, MIN_NUMBER, PERIODS


class Result:
    def __init__(self, raw_result):
        self.raw_result = raw_result
        self.errors = errors = []

        # Validate draw
        self.draw = draw = raw_result[0]
        if draw < 1:
            errors.append('draw must be greater than or equal to 1, given %s' % draw)

        # Validate date
        year = raw_result[1]
        month = raw_result[2]
        day = raw_result[3]
        try:
            self.date = datetime.date(year, month, day)
        except ValueError:
            errors.append('year, month and day must represent a valid date, given %s, %s and %s' % (year, month, day))

        # Validate period
        self.period = period = raw_result[4]
        if period not in PERIODS:
            errors.append('period must be one of %s, given %s' % (', '.join(PERIODS), period))

        # Validate number
        self.number = number = raw_result[5]
        if number < MIN_NUMBER or number > MAX_NUMBER:
            errors.append('number must be between %s and %s inclusive, given %s' % (MIN_NUMBER, MAX_NUMBER, number))

    def is_valid(self):
        return not self.errors

    def full_error_message(self):
        return '\n'.join(self.errors)

    def values(self):
        return { 'draw': self.draw, 'date': self.date, 'period': self.period, 'number': self.number }
