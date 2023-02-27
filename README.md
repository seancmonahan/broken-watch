# broken-watch

A broken date dial cannot adjust the day of the week and the day of the month independently.
For example, if it shows 'SUN, 3', you can only go to 'MON, 4' by winding the hands forward
by 24 hours, or to 'SAT, 2' if your watch allows you to wind the day/date backwards.
Thankfully, the number of days in a week (7) and the dial's number of days in a month (31)
are co-prime, so they cycle out of synchronization with a period of 217 (their LCM). This
means we can eventually get from any day/date to any other, albeit with a lot more effort
than if we could adjust the day of the week and the day of the month independently.

Using something called [Bézout's identity](https://en.wikipedia.org/wiki/Bézout's_identity),
the number of times the watch must be cycled to set a specific day-of-week/date can be calculated
in a closed-form expression.

I've not implemented the actual computation of a Bézout's identity for 7 and 31, but it
could be generalized by implementing the [extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm).

(A stopped day-date dial is still right about 1.68 times per year on average.)
