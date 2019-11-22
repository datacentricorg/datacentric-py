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

from __future__ import annotations
import datetime as dt


# TODO - this is a placeholder, implement


class LocalDateTime:
    """
    LocalDateTime is an immutable struct representing a date and time of day
    within the calendar, with no reference to a particular time zone.

    This class is inspired by NodaTime.LocalDateTime and follows the NodaTime
    naming conventions.
    """

    def __init__(self, year: int, month: int, day: int, hour: int = 0,
                 minute: int = 0, second: int = 0, millisecond: int = 0):
        self._dt = dt.datetime(year, month, day, hour, minute, second, microsecond=millisecond * 1000)

    def to_iso_int(self) -> int:
        iso_date = self._dt.year * 10_000 + self._dt.month * 100 + self._dt.day
        iso_time = self._dt.hour * 100_00_000 + self._dt.minute * 100_000 + \
                   self._dt.second * 1000 + self._dt.microsecond // 1000
        return iso_date * 100_00_00_000 + iso_time

    @classmethod
    def from_iso_int(cls, value: int) -> LocalDateTime:
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

        return cls(year, month, day, hour, minute, second, millisecond)
