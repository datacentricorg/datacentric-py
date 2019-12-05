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


class LocalTime(int, ABC):
    """
    Represents time of day to millisecond precision, with no reference to a
    particular date or time zone, and provides conversion to and from:

    * Integer hour, minute, second, and optional millisecond
    * Integer to millisecond precision in ISO hhmmssfff format
    * ISO string to millisecond precision in hh:mm:ss.fff format
    * Python dt.time
    """

    # --- METHODS

    @abstractmethod
    def abstract_class_guard(self) -> None:
        """
        Guard method to prevent this abstract base class from
        being instantiated.
        """
        pass

    # --- STATIC

    @classmethod
    def from_fields(cls, hour: int, minute: int, second: int,
                    millisecond: Optional[int] = None) -> Union[int, 'LocalTime']:
        """
        Convert hour to millisecond fields to LocalTime represented in hhmmssfff format.

        Millisecond field is optional. Zero value will be assumed if not specified.
        """

        # If millisecond is not specified, assume 0
        if millisecond is None:
            millisecond = 0

        # Convert to LocalTime represented in hhmmssfff format
        result: int = 10_000_000 * hour + 100_000 * minute + 1000 * second + millisecond

        # Validate and return
        cls.validate(result)
        return result

    @classmethod
    def to_fields(cls, value: Union[int, 'LocalTime']) -> Tuple[int, int, int, int]:
        """
        Convert LocalTime represented in hhmmssfff format to
        the tuple (hour, minute, second, millisecond).
        """

        # Perform fast validation to detect values out of range.
        # This will not detect errors such as Feb 31
        cls.validate(value)

        # Convert to tuple
        hour, minute, second, millisecond = cls.__to_fields_lenient(value)
        return hour, minute, second, millisecond

    @classmethod
    def from_str(cls, value: str) -> Union[int, 'LocalTime']:
        """
        Convert from string in ISO format without timezone suffix
        and up to 7 digits after decimal points for seconds.

        This method rounds the result to whole milliseconds.

        Examples:

        10:15:30
        10:15:30.1
        ...
        10:15:30.1234567 (will be rounded to whole milliseconds)
        """

        if not value[-1].isdigit():
            raise Exception(f'String {value} passed to LocalTime.from_str(...) method '
                            f'must not include timezone.')

        # Convert to datetime and set UTC timezone
        time_from_str: dt.time
        if '.' in value:
            # Has milliseconds
            time_from_str = dt.datetime.strptime(value, '%H:%M:%S.%f').time()
        else:
            # Does not have milliseconds
            time_from_str = dt.datetime.strptime(value, '%H:%M:%S').time()

        # Round the result to whole milliseconds
        rounded_time: dt.time = cls.__round_lenient(time_from_str)

        # Convert to LocalTime represented as int in hhmmssfff format
        result: Union[int, LocalTime] = cls.from_time(rounded_time)
        return result

    @classmethod
    def to_str(cls, value: Union[int, 'LocalTime']) -> str:
        """
        Convert to string in ISO format without timezone, with
        3 digits after decimal points for seconds, irrespective of
        how many digits are actually required.

        Example:

        10:15:30.500Z
        """

        # Convert to tuple
        hour, minute, second, millisecond = cls.__to_fields_lenient(value)

        # Convert to string in ISO format without timezone, with
        # 3 digits after decimal points for seconds, irrespective of
        # how many digits are actually required.
        result_to_microseconds: str = cls.to_time(value).strftime('%H:%M:%S.%f')
        result: str = result_to_microseconds[:-3]
        return result

    @classmethod
    def from_time(cls, value: dt.time) -> Union[int, 'LocalTime']:
        """
        Convert from dt.time.

        The argument time must not specify a timezone and will
        be rounded to whole milliseconds.
        """

        # Round the millisecond
        millisecond: int = round(value.microsecond / 1000.0)

        result: Union[int, 'LocalTime'] = LocalTime.from_fields(value.hour, value.minute, value.second, millisecond)
        return result

    @classmethod
    def to_time(cls, value: Union[int, 'LocalTime']) -> dt.time:
        """Convert to dt.time."""

        # Convert to tuple
        hour, minute, second, millisecond = cls.__to_fields_lenient(value)

        # The resulting dt.time must not have a timezone
        result: dt.time = dt.time(hour, minute, second, 1000 * millisecond)
        return result

    @classmethod
    def validate(cls, value: Union[int, 'LocalTime']) -> None:
        """
        Raise exception if the argument is not an int in ISO hhmmssfff format.
        """

        # Convert to tuple
        hour, minute, second, millisecond = cls.__to_fields_lenient(value)

        if not (0 <= hour <= 23):
            raise Exception(f'LocalTime {value} is not in hhmmssfff format. '
                            f'The hour {hour} should be in 0 to 23 range.')
        if not (0 <= minute <= 59):
            raise Exception(f'LocalTime {value} is not in hhmmssfff format. '
                            f'The minute {minute} should be in 0 to 59 range.')
        if not (0 <= second <= 59):
            raise Exception(f'LocalTime {value} is not in hhmmssfff format. '
                            f'The second {second} should be in 0 to 59 range.')
        if not (0 <= millisecond <= 999):
            raise Exception(f'LocalTime {value} is not in hhmmssfff format. '
                            f'The millisecond {millisecond} should be in 0 to 999 range.')

    @classmethod
    def __to_fields_lenient(cls, value: Union[int, 'LocalTime']) -> Tuple[int, int, int, int]:
        """
        Convert LocalTime stored as int in ISO hhmmssfff format to
        the tuple (hour, minute, second, millisecond).

        This method does not perform validation of its argument.
        """

        hour: int = value // 10_000_000
        value -= hour * 10_000_000
        minute: int = value // 100_000
        value -= minute * 100_000
        second: int = value // 1_000
        value -= second * 1_000
        millisecond: int = value

        return hour, minute, second, millisecond

    @classmethod
    def __round_lenient(cls, value: dt.time) -> dt.time:
        """
        Round the argument dt.time to whole milliseconds.

        This method does not perform validation of its argument.
        """

        # Round to whole millisecond
        rounded_microsecond: int = round(value.microsecond / 1000.0) * 1000

        result: dt.time = dt.time(
            value.hour,
            value.minute,
            value.second,
            rounded_microsecond,
            value.tzinfo
        )
        return result
