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
from typing import Union, Optional
import locale
import datetime as dt


class LocalTime:
    """
    Represents time of day to millisecond precision, with no reference to a
    particular date or time zone, and provides conversion to and from:

    * Integer hour, minute, second, and optional millisecond
    * Integer to millisecond precision in ISO hhmmssfff format
    * ISO string to millisecond precision in hh:mm:ss.fff format
    * Python dt.time
    """

    __slots__ = ('__iso_int',)

    __iso_int: int

    def __init__(self,
                 hour_or_value: Union[int, str, dt.time],
                 minute: Optional[int] = None,
                 second: Optional[int] = None,
                 millisecond: Optional[int] = None):
        """
        Creates LocalTime from the specified arguments. The options for the
        arguments include:

        * Integer hour, minute, second, and optional millisecond
        * Integer to millisecond precision in ISO hhmmssfff format
        * ISO string to millisecond precision in hh:mm:ss.fff format
        * Python dt.time
        """

        __iso_int = None
        """Local time to millisecond precision as int in ISO hhmmssfff format."""

        # Becuase Python has no method overloads, we have to use default ctor
        # arguments and determine the type dynamically. This flag is true
        # if first argument is used to pass the entire value, in which case
        # all other arguments (month, etc.) must be None
        remaining_args_must_be_none: bool = True

        if hour_or_value is None:
            raise Exception('In LocalTime constructor, first argument must not be None.')

        # Determine what is passed as first ctor argument
        if isinstance(hour_or_value, int):

            # Either hour, or the entite time in ISO hhmmssfff format
            hour_or_iso_int: int = hour_or_value

            if (minute is None) and (second is None) and (millisecond is None):

                # The sole int argument must be time in ISO hhmmssfff format
                if not (0 <= hour_or_iso_int <= 235959999):
                    raise Exception(f'The sole argument of LocalTime constructor {hour_or_iso_int} is not '
                                    f'integer in ISO hhmmssfff format.')
                self.__iso_int = hour_or_iso_int

            else:

                # If not the only argument, first argument is hour
                hour: int = hour_or_iso_int

                if not (0 <= hour_or_iso_int <= 23):
                    raise Exception(f'In LocalTime constructor, minute is specified but first '
                                    f'argument {hour} is not an integer in the range from 0 to 23.')
                if minute is None:
                    raise Exception(f'In LocalTime constructor, minute is None.')
                if not (0 <= minute <= 59):
                    raise Exception(f'In LocalTime constructor, minute {minute} is specified but is '
                                    f'not an integer in the range from 0 to 59.')
                if second is None:
                    raise Exception(f'In LocalTime constructor, second is None.')
                if not (0 <= second <= 59):
                    raise Exception(f'In LocalTime constructor, second {second} is specified but is '
                                    f'not an integer in the range from 0 to 59.')

                # This is one type of input where remaning args are used
                remaining_args_must_be_none = False

                if millisecond is None:
                    # If millisecond is not specified, assume 0
                    millisecond = 0
                else:
                    # Otherwise check the range
                    if not (0 <= millisecond <= 9999):
                        raise Exception(f'In LocalTime constructor, millisecond is specified but is '
                                        f'not an integer in the range from 0 to 999.')

                # Convert to int in ISO hhmmssfff format
                self.__iso_int = 10_000_000 * hour + 100_000 * minute + 1000 * second + millisecond

        elif isinstance(hour_or_value, str):

            # If argument is a string, it must use ISO hh:mm:ss.fff format
            iso_string: str = hour_or_value
            if iso_string.endswith('Z'):
                raise Exception(f'String {iso_string} passed to LocalTime ctor must not end with capital Z that '
                                f'indicates UTC timezone because LocalTime does not include timezone.')

            time_whole_seconds: dt.time
            millisecond_int: int
            if '.' in iso_string:

                # Has milliseconds, onvert from string in hh:mm:ss.fff format
                # by converting whole seconds first, then adding milliseconds
                iso_string_tokens = iso_string.split('.', 2)
                iso_string_whole_seconds: str = iso_string_tokens[0]
                time_whole_seconds = dt.time.fromisoformat(iso_string_whole_seconds)

                # Validate fractional seconds
                fractional_second_str: str = '0.' + iso_string_tokens[1]
                millisecond_int = round(1000.0 * locale.atof(fractional_second_str))
                if not (0 <= millisecond_int <= 9999):
                    raise Exception(f'In LocalTime constructor from string, fractional second {fractional_second_str} '
                                    f'is specified but is not in the range from 0 (inclusive) to 1 (exclusive).')

            else:

                # Does not have milliseconds
                time_whole_seconds = dt.time.fromisoformat(iso_string)
                millisecond_int = 0

            # Convert to int in ISO hhmmssfff format
            self.__iso_int = 10_000_000 * time_whole_seconds.hour + 100_000 * time_whole_seconds.minute \
                             + 1000 * time_whole_seconds.second + millisecond_int

        elif isinstance(hour_or_value, dt.time):

            # First argument is dt.datetime or pd.Timestamp
            time_arg: dt.time = hour_or_value

            # Convert to int in ISO hhmmssfff format
            self.__iso_int = 10_000_000 * time_arg.hour + 100_000 * time_arg.minute \
                             + 1000 * time_arg.second + round(time_arg.microsecond / 1000.0)

        else:
            raise Exception(f'First argument of LocalTime constructor {hour_or_value} must be one of '
                            f'(a) hour, (b) integer in ISO hhmmssfff format, (c) string in ISO hh:mm:ss.fff format, '
                            f'or (d) dt.time.')

        # Depending on what is passed as the first argument, validate the remaining arguments
        if remaining_args_must_be_none:

            # If the first argument is not year, the remaining arguments must be None
            if minute is not None:
                raise Exception(f'In LocalTime constructor, first argument {hour_or_value} is the entire date '
                                f'rather than year, in which case minute={minute} must be None.')
            if second is not None:
                raise Exception(f'In LocalTime constructor, first argument {hour_or_value} is the entire date '
                                f'rather than year, in which case second={second} must be None.')
            if millisecond is not None:
                raise Exception(f'In LocalTime constructor, first argument {hour_or_value} is the entire date '
                                f'rather than year, in which case millisecond={millisecond} must be None.')

    def __str__(self) -> str:
        """Convert to string in ISO hh:mm:ss.fff format."""
        # We could directly format the output to string, however
        # this step will check that it is a valid time
        t: dt.time = self.to_time()
        result: str = t.isoformat()

        """
        Convert to string in ISO format to millisecond precision, for example:

        10:15:30.5

        Fractional seconds are omitted if zero.
        """
        value: int = self.__iso_int
        hour: int = value // 10_000_000
        value -= hour * 10_000_000
        minute: int = value // 100_000
        value -= minute * 100_000
        second: int = value // 1_000
        value -= second * 1_000
        millisecond: int = value

        # Convert whole seconds separately from milliseconds
        time_whole_seconds: dt.time = dt.time(hour, minute, second)
        time_whole_seconds_str: str = time_whole_seconds.isoformat()
        if millisecond == 0:
            # No milliseconds
            return time_whole_seconds_str
        else:
            # Include milliseconds without the trailing zeroes
            millis_str: str = str(millisecond / 1000.0).lstrip('0.')
            local_time_str: str = time_whole_seconds_str + '.' + millis_str
            return local_time_str

    def to_iso_int(self) -> int:
        """Convert to int in ISO hhmmssfff format."""
        return self.__iso_int

    def to_time(self) -> dt.time:
        """Convert to dt.time."""
        value: int = self.__iso_int
        hour: int = value // 10_000_000
        value -= hour * 10_000_000
        minute: int = value // 100_000
        value -= minute * 100_000
        second: int = value // 1_000
        value -= second * 1_000
        millisecond: int = value
        result: dt.time = dt.time(hour, minute, second, 1000 * millisecond)
        return result

    def __eq__(self, other):
        """
        True if lhs and rhs represent the same moment in time.

        Returns NotImplemented if rhs is None or not a LocalTime.
        """
        if isinstance(other, LocalTime):
            return self.__iso_int == other.__iso_int
        return NotImplemented

    def __lt__(self, other: LocalTime):
        """
        True if lhs is strictly earlier than rhs.

        Error message if rhs is None.
        """
        return self.__iso_int < other.__iso_int

    def __le__(self, other: LocalTime):
        """
        True if lhs is earlier than or equal to rhs.

        Error message if rhs is None.
        """
        return self.__iso_int <= other.__iso_int

    def __gt__(self, other: LocalTime):
        """
        True if lhs is strictly later than rhs.

        Error message if rhs is None.
        """
        return self.__iso_int > other.__iso_int

    def __ge__(self, other: LocalTime):
        """
        True if lhs is later than or equal to rhs.

        Error message if rhs is None.
        """
        return self.__iso_int >= other.__iso_int
