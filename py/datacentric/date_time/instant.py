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
import datetime as dt
import pytz


class Instant:
    """
    Represents an instant on the global timeline in UTC timezone, with
    one millisecond resolution, and provides conversion to and from:

    * Int year, month, day, hour, minute, second, and millisecond in UTC
    * Int value of milliseconds since the Unix epoch
    * ISO string in yyy-mm-ddThh:mm:ss.fffZ format
    * Python dt.datetime
    * Pandas pd.timestamp
    """

    __slots__ = ('__unix_millis',)

    __unix_epoch: dt.datetime = dt.datetime.fromtimestamp(0, pytz.UTC)
    __unix_millis: int

    def __init__(self,
                 year_or_value: Union[int, str, dt.datetime],
                 month: Optional[int] = None,
                 day: Optional[int] = None,
                 hour: Optional[int] = None,
                 minute: Optional[int] = None,
                 second: Optional[int] = None,
                 millisecond: Optional[int] = None):
        """
        Creates Instant to millisecon precision from the specified
        arguments. The options for the arguments include:

        * Int year, month, day, hour, minute, second, and millisecond in UTC
        * Int value of milliseconds since the Unix epoch
        * ISO string in yyy-mm-ddThh:mm:ss.fffZ format
        * Python dt.datetime
        * Pandas pd.timestamp
        """

        __unix_millis = None
        """Milliseconds since Unix epoch."""

        # Becuase Python has no method overloads, we have to use default ctor
        # arguments and determine the type dynamically. This flag is true
        # if first argument is used to pass the entire value, in which case
        # all other arguments (month, etc.) must be None
        remaining_args_must_be_none: bool = True

        # Determine what is passed as first ctor argument
        if isinstance(year_or_value, int):

            # If first argument is int, it may be year or Unix epoch millis
            year_or_unix_millis: int = year_or_value

            if 1970 <= year_or_unix_millis <= 9999:

                # First argument is year if in the range from 1970 to 9999 (inclusive)
                year: int = year_or_unix_millis

                # This is one type of input where remaning args are used
                remaining_args_must_be_none = False

                # If the first argument is year, only millisecond is optional
                if month is None:
                    raise Exception(f'In Instant constructor, first argument {year} is year '
                                    f'in which case month must be specified.')
                if day is None:
                    raise Exception(f'In Instant constructor, first argument {year} is year '
                                    f'in which case day must be specified.')
                if hour is None:
                    raise Exception(f'In Instant constructor, first argument {year} is year '
                                    f'in which case hour must be specified.')
                if minute is None:
                    raise Exception(f'In Instant constructor, first argument {year} is year '
                                    f'in which case minute must be specified.')
                if second is None:
                    raise Exception(f'In Instant constructor, first argument {year} is year '
                                    f'in which case second must be specified.')

                # If millisecond is not specified, assume 0
                if millisecond is None:
                    millisecond = 0

                # Create dt.datetime in UTC timezone
                value: dt.datetime = dt.datetime(year, month, day, hour, minute, second, 1000 * millisecond,
                                                 pytz.UTC)

                # Round to the nearest whole milliseconds since Unix epoch
                self.__unix_millis = round((value - self.__unix_epoch).total_seconds() * 1000)

            elif year_or_unix_millis >= 0:

                # Otherwise first argument is milliseconds since Unix epoch
                self.__unix_millis = year_or_unix_millis

            else:
                raise Exception(f'First argument of Instant constructor {year_or_unix_millis} is negative.')

        elif isinstance(year_or_value, str):

            # If argument is a string, it must specify UTC (Z) timezone explicitly
            iso_string: str = year_or_value
            if not iso_string.endswith('Z'):
                raise Exception(f'Datetime string {iso_string} passed to Instant ctor must end with capital Z that '
                                f'indicates UTC timezone.')

            # Convert to datetime and set UTC timezone
            dtime_from_str: dt.datetime
            if '.' in iso_string:
                # Has milliseconds
                dtime_from_str = dt.datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                # Does not have milliseconds
                dtime_from_str = dt.datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%SZ')

            # Set tzinfo to the standard UTC singleton from pytz module
            dtime_from_str = dtime_from_str.replace(tzinfo=pytz.UTC)

            # Round to the nearest whole milliseconds since Unix epoch
            self.__unix_millis = round((dtime_from_str - self.__unix_epoch).total_seconds() * 1000)

        elif isinstance(year_or_value, dt.datetime):

            # First argument is dt.datetime or pd.Timestamp
            dtime: dt.datetime = year_or_value

            # Check that timezone is UTC, error message otherwise
            if dtime.utcoffset().microseconds != 0:
                raise Exception(f'Datetime {dtime} passed to Instant ctor is not in UTC timezone.')

            # Round to the nearest whole milliseconds since Unix epoch.
            #
            # Because:
            #
            # * Time zone info (tzinfo) is abstract class in Python
            # * There are several different singletons representing UTC, and
            # * Comparison will will fail if different instances are passed,
            #
            # we must use the instance of tzinfo from the external object here,
            # which was already verified to have 0 offset relative to UTC
            unix_epoch: dt.datetime = dt.datetime.fromtimestamp(0, dtime.tzinfo)
            self.__unix_millis = round((dtime - unix_epoch).total_seconds() * 1000)

        else:
            raise Exception(f'First argument of Instant constructor {year_or_value} must be one of '
                            f'(a) year, (b) milliseconds since Unix epoch, (c) dt.datetime, or (d) pd.Timestamp.')

        # Depending on what is passed as the first argument, validate the remaining arguments
        if remaining_args_must_be_none:

            # If the first argument is not year, the remaining arguments must be None
            if month is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case month={month} must be None.')
            if day is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case day={day} must be None.')
            if hour is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case hour={hour} must be None.')
            if minute is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case minute={minute} must be None.')
            if second is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case second={second} must be None.')
            if millisecond is not None:
                raise Exception(f'In Instant constructor, first argument {year_or_value} is the entire datetime '
                                f'rather than year, in which case millisecond={millisecond} must be None.')

    def __str__(self) -> str:
        """
        Convert to string in ISO format with UTC (Z) timezone suffix
        to millisecond precision, for example:

        2003-05-01T10:15:30.5Z

        Fractional seconds are omitted if zero.
        """
        dtime: dt.datetime = self.to_datetime()
        second_str: str = dtime.strftime('%Y-%m-%dT%H:%M:%S')
        if dtime.microsecond == 0:
            # No milliseconds
            return second_str + 'Z'
        else:
            # Include milliseconds without the trailing zeroes
            millis_str: str = str(dtime.microsecond / 1.0e6).lstrip('0.')
            result: str = second_str + '.' + millis_str + 'Z'
            return result

    def to_unix_millis(self) -> int:
        """
        Convert to the number of milliseconds since Unix epoch.

        Because Instant is rounded to the nearest millisecond,
        the returned value is always int.
        """
        return self.__unix_millis

    def to_datetime(self) -> dt.datetime:
        """
        Convert to dt.datetime in UTC timezone.
        """
        # Convert milliseconds from Unix epoch to seconds, then construct the date
        # and replace timezone with pytz.UTC which is more standard
        return dt.datetime.utcfromtimestamp(self.__unix_millis / 1000.0).replace(tzinfo=pytz.UTC)
