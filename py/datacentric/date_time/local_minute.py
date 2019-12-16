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
from typing import Union, Optional, Tuple
import datetime as dt


class LocalMinute(int, ABC):
    """
    Represents minute of the day from 00:00 to 23:59, with no reference to a
    particular date or time zone, and provides conversion to and from:

    * Integer hour and minute
    * Integer in hhmm format
    * String in hh:mm format
    * Python dt.time (when used as input, must fall exactly on the minute)
    """

    # --- METHODS

    @abstractmethod
    def abstract_class_guard(self) -> None:
        """
        Guard method to prevent this abstract base class from
        being instantiated.
        """
        pass

    # --- CLASS

    @classmethod
    def from_fields(cls, hour: int, minute: int) -> Union[int, 'LocalMinute']:
        """
        Convert hour and minute fields to LocalMinute represented as int in hhmm format.
        """

        # Convert to LocalMinute represented as int in hhmm format
        result: int = 100 * hour + minute

        # Perform validation to detect out of range values
        cls.validate(result)

        return result

    @classmethod
    def to_fields(cls, value: Union[int, 'LocalMinute']) -> Tuple[int, int]:
        """
        Convert LocalMinute represented as int in hhmm format to
        the tuple (hour, minute).
        """

        # Perform validation to detect out of range values
        cls.validate(value)

        # Convert to tuple
        hour, minute = cls.__to_fields_lenient(value)
        return hour, minute

    @classmethod
    def from_str(cls, value: str) -> Union[int, 'LocalMinute']:
        """
        Convert from string in hh:mm without timezone suffix.

        Example: 10:15
        """

        if not value[-1].isdigit():
            raise Exception(f'String {value} passed to LocalMinute.from_str(...) method '
                            f'must not include timezone.')

        time_from_str = dt.datetime.strptime(value, '%H:%M').time()

        # Convert to LocalMinute represented as int in hhmmssfff format
        result: Union[int, LocalMinute] = cls.from_time(time_from_str)
        return result

    @classmethod
    def to_str(cls, value: Union[int, 'LocalMinute']) -> str:
        """
        Convert to string in hh:mm format without timezone.

        Example: 10:15
        """

        # Convert to tuple
        hour, minute = cls.__to_fields_lenient(value)

        # Convert to string in ISO format without timezone
        result: str = cls.to_time(value).strftime('%H:%M')
        return result

    @classmethod
    def from_time(cls, value: dt.time) -> Union[int, 'LocalMinute']:
        """
        Convert from dt.time.

        The argument time must not specify a timezone and must
        fall exactly on the minute
        """
        if value.tzinfo != None:
            raise Exception(f'Time passed to LocalMinute.from_time(cls) has timezone {value.tzinfo}.')
        if value.second != 0 or value.microsecond != 0:
            raise Exception(f'Value {value} does not fall exactly on the minute.')

        result: Union[int, 'LocalMinute'] = LocalMinute.from_fields(value.hour, value.minute)
        return result

    @classmethod
    def to_time(cls, value: Union[int, 'LocalMinute']) -> dt.time:
        """Convert to dt.time."""

        # Convert to tuple
        hour, minute = cls.__to_fields_lenient(value)

        # The resulting dt.time must not have a timezone
        result: dt.time = dt.time(hour, minute, 0, 0)
        return result

    @classmethod
    def validate(cls, value: Union[int, 'LocalMinute']) -> None:
        """
        Raise exception if the argument is not None and is not an int
        in hhmm format.
        """

        # If None, return before doing other checks
        if value is None:
            return

        # Convert to tuple
        hour, minute = cls.__to_fields_lenient(value)

        if not (0 <= hour <= 23):
            raise Exception(f'LocalMinute {value} is not in hhmm format. '
                            f'The hour {hour} should be in 0 to 23 range.')
        if not (0 <= minute <= 59):
            raise Exception(f'LocalMinute {value} is not in hhmm format. '
                            f'The minute {minute} should be in 0 to 59 range.')

    @classmethod
    def __to_fields_lenient(cls, value: Union[int, 'LocalMinute']) -> Tuple[int, int]:
        """
        Convert LocalMinute stored as int in hhmm format to
        the tuple (hour, minute).

        This method does not perform validation of its argument.
        """

        hour: int = value // 100
        value -= hour * 100
        minute: int = value

        return hour, minute
