#!/usr/bin/env python

from __future__ import annotations
from typing import NamedTuple
import datetime
from functools import singledispatchmethod


class DateDial(NamedTuple):
    day: int
    date: int

    def __add__(self, n: int) -> DateDial:
        '''Turn the dial forwards `n` clicks.'''
        return DateDial((self.day + n) % 7, (self.date - 1 + n) % 31 + 1)

    @singledispatchmethod
    def __sub__(self, other):
        raise NotImplementedError(f'__sub__ not implemented for type(other) {type(other)}')

    @__sub__.register
    def __sub__integer(self, n: int):
        return self + -n

    def __str__(self) -> str:
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        days = [day[:3].upper() for day in days]  # Trim to three uppercase letters
        print(days)
        return f'{days[self.day]}, {self.date}'

    @classmethod
    def fromdate(cls, d: datetime.date) -> DateDial:
        return cls(d.isoweekday() % 7, d.day)


@DateDial.__sub__.register
def clicks_from(self, other: DateDial):
    '''Calculate how many 'clicks' to get from DateDial `other` to self'''
    day_delta = (self.day - other.day) % 7
    date_delta = (self.date - other.date) % 31

    (n1, n2) = (7, 31)
    (m1, m2) = bezouts_identity(n1, n2)     # 9, -2

    # ((day_delta * -62) + (date_delta * 63)) modulo 217
    return (day_delta * m2 * n2 + date_delta * m1 * n1) % (n1 * n2)


def bezouts_identity(n1, n2):
    if n1 == 7 and n2 == 31:
        return (9, -2)

    raise NotImplementedError("Bézout's identity calculation not implemented yet"
                              " for anything besides 7, 31")


def count_broken_dial_corrent(dial: DateDial, year: int = 2018) -> int:
    d = datetime.date(year, 1, 1)

    count = 0
    delta_one_day = datetime.timedelta(1)

    while True:
        if DateDial.fromdate(d) == dial:
            count += 1

        d += delta_one_day

        if d.year != year:
            return count


if __name__ == "__main__":
    dd = DateDial.fromdate(datetime.date.today())
