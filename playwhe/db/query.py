from sqlalchemy import case, select

from .schema import results


PERIODS_DESC = {
    'EM': 3,
    'AM': 2,
    'AN': 1,
    'PM': 0
}


def select_last_result():
    return select([results]).\
        order_by(results.c.date.desc()).\
        order_by(case(PERIODS_DESC, value=results.c.period)).\
        order_by(results.c.draw.desc()).\
        limit(1)
