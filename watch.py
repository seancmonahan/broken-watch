#!/usr/bin/env python

from __future__ import annotations
from typing import Any, List, Iterable

from dataclasses import dataclass
import datetime
import itertools


@dataclass(order=True, frozen=True)
class DateDial:
    day: int
    date: int

    def click(self, n: int) -> DateDial:
        return DateDial((self.day + n) % 7, (self.date - 1 + n) % 31 + 1)

    @classmethod
    def fromdate(cls, d: datetime.date) -> DateDial:
        return cls(d.isoweekday() % 7, d.day)


def head(iterable: Iterable[Any], n: int) -> List[Any]:
    return list(itertools.islice(iterable, n))


def clicks_for_day(current: int, want: int) -> Iterable[int]:
    return itertools.count((want - current) % 7, 7)


def clicks_for_date(current, want) -> Iterable[int]:
    return itertools.count((want - current) % 31, 31)


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
