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

from abc import ABC, abstractmethod
import datetime as dt
import numpy as np

# TODO - implementation is incomplete


class LocalMinute(int, ABC)
    """
    LocalMinute is an immutable struct representing a time of day
    to one minute precision, with no reference to a particular calendar,
    time zone or date.

    This class is not part of NodaTime but is inspired by NodaTime.LocalTime
    and follows the NodaTime naming conventions.
    """

    def __init__(self, hour: int, minute: int):
        """
        Creates local time to one minute precision from the specified
        hour and minute.
        """

        if hour < 0 or hour > 23:
            raise Exception(f'Hour {hour} is not between 0 and 23.')
        if minute < 0 or minute > 59:
            raise Exception(f'Minute {minute} is not between 0 and 59.')
        self.hour = hour
        self.minute = minute

    def to_time(self) -> dt.time:
        return dt.time(self.hour, self.minute)

    @property
    def minute_of_day(self) -> int:
        return self.hour * 60 + self.minute

    def to_iso_int(self) -> int:
        return self.hour * 100 + self.minute

    @classmethod
    def from_iso_int(cls, value: int) -> LocalMinute:
        hour = value // 100
        value -= hour * 100
        minute = value
        return cls(hour, minute)

    def __str__(self):
        """
        Convert LocalMinute to ISO 8601 string in hh:mm format.
        """
        return f'{self.hour:02}:{self.minute:02}'
