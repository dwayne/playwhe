from collections import namedtuple
import re


# Each result has the format:
#
#   <strong> Draw #: </strong>[draw]<br>
#   <strong> Date: </strong>[dd]-[mmm]-[yy]<br>
#   <strong> Mark Drawn: </strong>[number]<br>
#   <strong> Drawn at: </strong>[period]
RESULT_RE = r'Draw #: </strong>(\d+).*? Date: </strong>(\d{1,2})-%s-%s.*? Mark Drawn: </strong>(\d+).*? Drawn at: </strong>(EM|AM|AN|PM)'


def parse(html, year, month, yy, mmm):
    matches = re.findall(RESULT_RE % (mmm, yy), html, re.IGNORECASE)

    return [_norm(m, year, month) for m in matches]


RawResult = namedtuple('RawResult', ['draw', 'year', 'month', 'day', 'period', 'number'])


def _norm(match, year, month):
    draw = int(match[0])
    day = int(match[1])
    number = int(match[2])
    period = match[3].upper()

    return RawResult(draw, year, month, day, period, number)
