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


class LocalDate:
    """
    LocalDate is an immutable struct representing a date within the calendar,
    with no reference to a particular time zone or time of day.

    This class is inspired by NodaTime.LocalDate and follows the NodaTime
    naming conventions.
    """

    def __init__(self, year: int, month: int, day: int):
        self._date = dt.date(year, month, day)

    def __str__(self):
        return str(self._date)

    def to_iso_int(self) -> int:
        return self._date.year * 10_000 + self._date.month * 100 + self._date.day

    @classmethod
    def from_iso_int(cls, value: int) -> LocalDate:
        year = value // 100_00
        value -= year * 100_00
        month = value // 100
        value -= month * 100
        day = value
        return cls(year, month, day)
