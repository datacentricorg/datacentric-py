# Copyright (C) 2013-present The DataCentric Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime as dt
from datacentric.date_time.local_minute import LocalMinute

# Convert to static methods of utility classes

def date_to_iso_int(value: dt.date) -> int:
    return value.year * 10_000 + value.month * 100 + value.day


def time_to_iso_int(value: dt.time) -> int:
    # todo: microseconds rounding
    return value.hour * 100_00_000 + value.minute * 100_000 + value.second * 1000 + value.microsecond * 1000


def date_time_to_iso_int(value: dt.datetime) -> int:
    iso_date = value.year * 10_000 + value.month * 100 + value.day
    iso_time = value.hour * 100_00_000 + value.minute * 100_000 + value.second * 1000 + value.microsecond * 1000
    return iso_date * 100_00_00_000 + iso_time


def minute_to_iso_int(value: LocalMinute) -> int:
    return value.hour * 100 + value.minute


def iso_int_to_date(value: int) -> dt.date:
    year = value // 100_00
    value -= year * 100_00
    month = value // 100
    value -= month * 100
    day = value
    return dt.date(year, month, day)


def iso_int_to_date_time(value: int) -> dt.datetime:
    iso_date = value // 100_00_00_000
    iso_time = value - 100_00_00_000 * iso_date

    year = iso_date // 100_00
    iso_date -= year * 100_00
    month = iso_date // 100
    iso_date -= month * 100
    day = iso_date

    hour = iso_time // 100_00_000
    iso_time -= hour * 100_00_000
    minute = iso_time // 100_000
    iso_time -= minute * 100_000
    second = iso_time // 1000
    iso_time -= second * 1000
    millisecond = iso_time

    return dt.datetime(year, month, day, hour, minute, second, millisecond * 1000)


def iso_int_to_local_minute(value: int) -> LocalMinute:
    hour = value // 100
    value -= hour * 100
    minute = value
    return LocalMinute(hour, minute)


def iso_int_to_time(value: int) -> dt.time:
    hour = value // 100_00_000
    value -= hour * 100_00_000
    minute = value // 100_000
    value -= minute * 100_000
    second = value // 1000
    value -= second * 1000
    millisecond = value
    return dt.time(hour, minute, second, millisecond * 1000)
