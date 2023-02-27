#!/usr/bin/env python

from __future__ import annotations
from typing import NamedTuple, List
import datetime
from functools import singledispatchmethod


class BrokenDateDial(NamedTuple):
    """Representation of a watch whose day/date display cannot be independently adjusted.
    `day` is an integer ∈ [0, 6], where 0 is Sunday, 1 is Monday, ... 6 is Saturday.
    `date` is an integer ∈ [1, 31], the day of the month.

    A broken date dial cannot adjust the day of the week and the day of the month independently.
    For example, if it shows 'SUN, 3', you can only go to 'MON, 4' or 'SAT, 2'.
    Thankfully, the number of days in a week (7) and the dial's number of days in a month (31)
    are co-prime, so they cycle out of synchronization with a period of 217 (their LCM). This
    means we can eventually get from any day/date to any other, albeit with a lot more effort
    than if we could adjust the day of the week and the day of the month independently.
    """

    day: int
    date: int

    @classmethod
    def fromdate(cls, d: datetime.date) -> BrokenDateDial:
        return cls(d.isoweekday() % 7, d.day)

    def __add__(self, n: int) -> BrokenDateDial:
        """Turn the dial forwards `n` clicks."""
        return BrokenDateDial((self.day + n) % 7, (self.date - 1 + n) % 31 + 1)

    @singledispatchmethod
    def __sub__(self, other):
        raise NotImplementedError(
            f"__sub__ not implemented for type(other) {type(other)}"
        )

    # @__sub__.register  # singledispatchmethod doesn't support ForwardRef('BrokenDateDial')
    def _sub__integer(self, n: int) -> BrokenDateDial:
        """Turn the dial backwards `n` clicks"""
        return self + -n

    # @__sub__.register  # Likewise here
    # doesn't matter whether we use `BrokenDateDial` or `'BrokenDateDial'` (string annotation)
    # @singledispatchmethod doesn't play well with NamedTuple, the annotated namedtuple class
    # when trying to dispatch on the class within which the method is defined.
    def clicks_from(self, other: BrokenDateDial) -> List[int]:
        """Calculate how many 'clicks' to get from BrokenDateDial `other` to self.

        Registered as single-dispatch on __sub__(other: BrokenDateDial)"""
        day_delta = (self.day - other.day) % 7
        date_delta = (self.date - other.date) % 31

        (n1, n2) = (7, 31)
        (m1, m2) = bezouts_identity(n1, n2)  # 9, -2

        # ((day_delta * -62) + (date_delta * 63)) modulo 217
        return (day_delta * m2 * n2 + date_delta * m1 * n1) % (n1 * n2)

    def __str__(self) -> str:
        days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        days = [day[:3].upper() for day in days]  # Trim to three uppercase letters
        return f"{days[self.day]}, {self.date}"


# We have to register single dispatch outside the class for BrokenDateDial.clicks_from,
# and we register _sub__integer here too to keep them together, not because it needs to be
# except that it returns a BrokenDateDial. Although we're not dispatching on the return type,
# the way the singledispathmethod decorator and __future__.annotations interact means
# that Python doesn't know of BrokenDateDial's existance within the decorator.
# I wonder if there's a way to get Python to support this...
BrokenDateDial.__sub__.register(BrokenDateDial.clicks_from)
BrokenDateDial.__sub__.register(BrokenDateDial._sub__integer)


def bezouts_identity(n1, n2):
    if n1 == 7 and n2 == 31:
        return (9, -2)

    raise NotImplementedError(
        "Bézout's identity calculation not implemented yet"
        " for anything besides 7, 31"
    )


def count_broken_dial_correct(dial: BrokenDateDial, year: int = 2018) -> int:
    """Count how often `dial` would be correct over the entire year `year`.

    For example, count_broken_dial_correct((0, 23), 2020) calculates how many
    Sundays (0) the 23rd (23) there are in the year 2020."""
    count = 0
    delta_one_day = datetime.timedelta(1)

    d = datetime.date(year, 1, 1)
    while True:
        if BrokenDateDial.fromdate(d) == dial:
            count += 1

        d += delta_one_day

        if d.year != year:
            return count


if __name__ == "__main__":
    dd = BrokenDateDial.fromdate(datetime.date.today())
