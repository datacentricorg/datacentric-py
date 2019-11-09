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

# TODO - implementation is incomplete


class LocalMinute:
    """
    LocalMinute is an immutable struct representing a time of day
    to one minute precision, with no reference to a particular calendar,
    time zone or date.

    This class is not part of NodaTime but is inspired by NodaTime.LocalTime
    and follows the NodaTime naming conventions.
    """

    hour: int
    minute: int

    def __init__(self, hour: int, minute: int):
        """
        Creates local time to one minute precision from the specified
        hour and minute.
        """

        if hour < 0 or hour > 23:
            raise AttributeError(f'Hour {hour} is not between 0 and 23.')
        if minute < 0 or minute > 59:
            raise AttributeError(f'Minute {minute} is not between 0 and 59.')
        self.hour = hour
        self.minute = minute

    def to_time(self) -> dt.time:
        return dt.time(self.hour, self.minute)

    @property
    def minute_of_day(self) -> int:
        return self.hour * 60 + self.minute

    def __eq__(self, other):
        """
        Compares two local times for equality, by checking whether
        they represent the exact same local time, down to the tick.
        """
        if isinstance(other, LocalMinute):
            return self.minute_of_day == other.minute_of_day
        return NotImplemented

    def __lt__(self, other: LocalMinute):
        """
        Compares two LocalMinute values to see if the left one
        is strictly earlier than the right one.
        """
        return self.minute_of_day < other.minute_of_day

    def __le__(self, other: LocalMinute):
        """
        Compares two LocalMinute values to see if the left one
        is earlier than or equal to the right one.
        """
        return self.minute_of_day <= other.minute_of_day

    def __gt__(self, other: LocalMinute):
        """
        Compares two LocalMinute values to see if the left one
        is strictly later than the right one.
        """
        return self.minute_of_day > other.minute_of_day

    def __ge__(self, other: LocalMinute):
        """
        Compares two LocalMinute values to see if the left one
        is later than or equal to the right one.
        """
        return self.minute_of_day >= other.minute_of_day

    def __str__(self):
        """
        Convert LocalMinute to ISO 8601 string in hh:mm format.
        """
        return f'{self.hour:02}:{self.minute:02}'
