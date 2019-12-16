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
import pytz


class Instant(dt.datetime, ABC):
    """
    Represents an instant on the global timeline in UTC timezone, with
    one millisecond resolution, and provides conversion to and from:

    * Int year, month, day, hour, minute, second, and millisecond in UTC
    * Int value of milliseconds since the Unix epoch
    * ISO string in yyy-mm-ddThh:mm:ss.fffZ format
    * Python dt.datetime
    * Pandas pd.timestamp
    """

    __unix_epoch: dt.datetime = dt.datetime.fromtimestamp(0, pytz.UTC)

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
    def from_fields(cls,
                    year: int,
                    month: int,
                    day: int,
                    hour: int,
                    minute: int,
                    second: int,
                    millisecond: Optional[int] = None) -> Union[dt.datetime, 'Instant']:
        """
        Creates Instant represented as dt.datetime to millisecond precision from
        the the fields from year to millisecond.

        Millisecond field is optional. Zero value will be assumed if not specified.
        """

        # If millisecond is not specified, assume 0
        if millisecond is None:
            millisecond = 0

        # Create dt.datetime in UTC timezone
        result: dt.datetime = dt.datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            1000 *
            millisecond,
            pytz.UTC)
        return result

    @classmethod
    def to_fields(cls, value: Union[dt.datetime, 'Instant']) -> Tuple[int, int, int, int, int, int, int]:
        """
        Convert Instant to millisecond precision
        the tuple (hour, minute, second, millisecond).
        """

        # Perform fast validation to detect values out of range.
        # This will not detect errors such as Feb 31
        cls.validate(value)

        # Calculate millisecond from microsecond
        millisecond: int = round(value.microsecond / 1000.0)

        # Return the tuple
        return value.year, value.month, value.day, value.hour, value.minute, value.second, millisecond

    @classmethod
    def from_str(cls, value: str) -> Union[dt.datetime, 'Instant']:
        """
        Convert from string in ISO format with UTC (Z) timezone suffix
        and up to 7 digits after decimal points for seconds.

        This method rounds the result to whole milliseconds.

        Examples:

        2003-05-01T10:15:30Z
        2003-05-01T10:15:30.1Z
        ...
        2003-05-01T10:15:30.1234567Z (will be rounded to whole milliseconds)
        """

        if not value.endswith('Z'):
            raise Exception(f'String {value} passed to Instant.from_str(...) method '
                            f'must end with capital Z that indicates UTC timezone.')

        # Convert to datetime and set UTC timezone
        dtime_from_str: dt.datetime
        if '.' in value:
            # Has milliseconds
            dtime_from_str = dt.datetime.strptime(
                value, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            # Does not have milliseconds
            dtime_from_str = dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

        # Set tzinfo to the standard UTC singleton from pytz module
        result: dt.datetime = dtime_from_str.replace(tzinfo=pytz.UTC)

        # Round the result to whole milliseconds
        result = cls.round(result)
        return result

    @classmethod
    def to_str(cls, value: Union[dt.datetime, 'Instant']) -> str:
        """
        Convert to string in ISO format with UTC (Z) timezone suffix
        and 3 digits after decimal points for seconds, irrespective of
        how many digits are actually required.

        Example:

        2003-05-01T10:15:30.500Z
        """

        # Ensure the argument is in UTC and does not have fractional
        # milliseconds
        cls.validate(value)

        # Convert to string in ISO format with UTC (Z) timezone suffix
        # and 3 digits after decimal points for seconds, irrespective of
        # how many digits are actually required.
        result_to_microseconds: str = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        result: str = result_to_microseconds[:-3] + 'Z'
        return result

    @classmethod
    def from_unix_millis(
            cls, unix_millis: int) -> Union[dt.datetime, 'Instant']:
        """
        Convert milliseconds since Unix epoch Instant stored as dt.datetime
        in UTC timezone.
        """
        # Convert milliseconds from Unix epoch to seconds, then construct the date
        # and replace timezone with pytz.UTC which is more standard
        return dt.datetime.utcfromtimestamp(
            unix_millis / 1000.0).replace(tzinfo=pytz.UTC)

    @classmethod
    def to_unix_millis(cls, value: Union[dt.datetime, 'Instant']) -> int:
        """
        Convert Instant stored as dt.datetime in UTC timezone to
        milliseconds since Unix epoch, rounding the value to
        whole milliseconds.

        Error message if the argument has fractional milliseconds,
        use Instant.round(value) to remove.
        """

        # Ensure the argument is in UTC and does not have fractional
        # milliseconds
        cls.validate(value)

        # Convert to milliseconds since Unix epoch and round to whole
        # milliseconds. Because we cannot subtract datetimes with two
        # different instances of tzinfo, even if both are UTC, we
        # cannot use a class variable for unix_epoch. It has to be
        # created in the argument timezone instead.
        unix_epoch: dt.datetime = dt.datetime.fromtimestamp(0, value.tzinfo)
        result: int = round((value - unix_epoch).total_seconds() * 1000)
        return result

    @classmethod
    def round(cls, value: Union[dt.datetime, 'Instant']
              ) -> Union[dt.datetime, 'Instant']:
        """
        Round the argument to whole milliseconds.

        This method checks that the argument is in UTC.
        """

        # Check that Instant is in UTC before rounding
        cls.check_in_utc(value)
        rounded_microsecond: int = round(value.microsecond / 1000.0) * 1000

        result: dt.datetime = dt.datetime(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
            rounded_microsecond,
            value.tzinfo
        )
        return result

    @classmethod
    def validate(cls, value: Union[dt.datetime, 'Instant']) -> None:
        """
        Raise exception if one of the following is true:

        * Instant is not None and has timezone other than UTC
        * Instant is not None and has no timezone
        * Instant is not None and has fractional milliseconds
          (use Instant.round(...) to remove)
        """

        # Check that either value is None, or timezone is UTC
        cls.check_in_utc(value)

        # Check that either value is None, or Instant has no fractional milliseconds
        cls.check_whole_millis(value)

    @classmethod
    def check_in_utc(cls, value: Union[dt.datetime, 'Instant']) -> None:
        """
        Raise exception if value is not None, and is not in UTC timezone.

        This method does not check if the argument has fractional Unix
        milliseconds.
        """

        # If None, return before doing other checks
        if value is None:
            return

        # Check that tzinfo is not None
        if value.tzinfo is None:
            raise Exception(f'Instant {cls.__to_str_lenient(value)} has tzinfo=None. '
                            f'Instant values must have tzinfo that has zero offset '
                            f'to UTC, such as pytz.UTC')

        # Because:
        #
        # * Time zone info (tzinfo) is abstract class in Python
        # * There are several different singletons representing UTC, and
        # * Comparison will will fail if different instances are passed,
        #
        # we must use UTC offset instead of comparing timezone value.
        if value.utcoffset().microseconds != 0:
            raise Exception(f'Instant {cls.__to_str_lenient(value)} is not in UTC. '
                            f'Instant values must have tzinfo that has zero offset '
                            f'to UTC, such as pytz.UTC')

    @classmethod
    def check_whole_millis(cls, value: Union[dt.datetime, 'Instant']) -> None:
        """
        Return true if value is either None, or has no fractional milliseconds.

        This method does not check if the argument is in UTC.
        """

        # If None, return before doing other checks
        if value is None:
            return

        # Convert to milliseconds since Unix epoch and round to whole
        # milliseconds
        unix_epoch: dt.datetime = dt.datetime.fromtimestamp(0, value.tzinfo)
        unix_millis: float = (value - unix_epoch).total_seconds() * 1000
        rounded_unix_millis: int = round(unix_millis)

        # Return false if more than roundoff tolerance
        if abs(unix_millis - rounded_unix_millis) >= 1e-10:
            raise Exception(f'Instant {cls.__to_str_lenient(value)} has fractional milliseconds. Valid '
                f'Instant values must have whole milliseconds to ensure that no loss of precision '
                f'occurs during serialization roundtrip. Use Instant.round(...) to remove.')

    @classmethod
    def __to_str_lenient(cls, value: Union[dt.datetime, 'Instant']) -> str:
        """
        This method performs no validation before converting to string.
        It should be used for error messages only.
        """

        # Lenient conversion to string without controlling
        # for timezone or precision. Use for error messages
        # only.
        result: str = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return result
