import re

from ..common import Result, Results


# Each result has the format:
#
#   <strong> Draw #: </strong>[draw]<br>
#   <strong> Date: </strong>[dd]-[mmm]-[yy]<br>
#   <strong> Mark Drawn: </strong>[number]<br>
#   <strong> Drawn at: </strong>[period]
RESULT_RE = r'Draw #: </strong>(\d+).*? Date: </strong>(\d{1,2})-%s-%s.*? Mark Drawn: </strong>(\d+).*? Drawn at: </strong>(EM|AM|AN|PM)'


def parse(html, params):
    matches = re.findall(RESULT_RE % (params.mmm, params.yy), html, re.IGNORECASE)

    return Results(Result(m[0], params.year, params.month, m[1], m[3], m[2]) for m in matches)
