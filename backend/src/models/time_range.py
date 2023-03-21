from enum import Enum


class Interval(str, Enum):
    one_minute = "1m"
    two_minutes = "2m"
    five_minutes = "5m"
    one_hour = "1h"

    one_day = "1d"
    five_days = "5d"


# 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo


class Period(Enum):

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, interval: Interval):
        self.interval = interval

    # days
    one_day = "1d", Interval.one_minute
    five_days = "5d", Interval.five_minutes
    # months
    one_month = "1mo", Interval.one_hour
    three_months = "3mo", Interval.one_hour
    six_months = "6mo", Interval.one_day
    # year
    one_year = "1y", Interval.one_day
    two_years = "2y", Interval.one_day
    five_years = "5y", Interval.one_day
    ten_years = "10y", Interval.one_day
