from sqlalchemy import bindparam, case, select

from .schema import marks, results


def select_marks():
    return select([marks])


def select_mark():
    return select([marks]).\
        where(marks.c.number == bindparam('number')).\
        limit(1)


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
