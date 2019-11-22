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


class LocalTime:
    """
    LocalTime is an immutable struct representing a time of day, with no reference
    to a particular calendar, time zone or date.

    This class is inspired by NodaTime.LocalTime and follows the NodaTime
    naming conventions.
    """

    def __init__(self, hour: int, minute: int, second: int = 0, milliseconds: int = 0):
        self._time = dt.time(hour, minute, second, microsecond=milliseconds * 1000)

    def to_iso_int(self) -> int:
        # todo: microseconds rounding
        return self._time.hour * 100_00_000 + self._time.minute * 100_000 + \
               self._time.second * 1000 + self._time.microsecond // 1000

    @classmethod
    def from_iso_int(cls, value: int) -> LocalTime:
        hour = value // 100_00_000
        value -= hour * 100_00_000
        minute = value // 100_000
        value -= minute * 100_000
        second = value // 1000
        value -= second * 1000
        millisecond = value
        return cls(hour, minute, second, millisecond)
