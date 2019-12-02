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


class LocalDate:
    """
    Represents a date within the calendar, with no reference to a particular
    time zone or time of day, and provides conversion to and from:

    * Integer year, month, and day of month
    * Integer in ISO yyyymmdd format
    * ISO string in yyyy-mm-dd format
    * Python dt.date
    """

    __slots__ = ('__iso_int',)

    __iso_int: int

    def __init__(self,
                 year_or_value: Union[int, str, dt.date],
                 month: Optional[int] = None,
                 day: Optional[int] = None):
        """
        Creates LocalDate from the specified arguments. The options for the
        arguments include:

        * Integer year, month, and day of month
        * Integer in ISO yyyymmdd format
        * ISO string in yyyy-mm-dd format
        * Python dt.date
        """

        __iso_int = None
        """Local date as int in ISO yyyymmdd format."""

        # Becuase Python has no method overloads, we have to use default ctor
        # arguments and determine the type dynamically. This flag is true
        # if first argument is used to pass the entire value, in which case
        # all other arguments (month, etc.) must be None
        remaining_args_must_be_none: bool = True

        # Determine what is passed as first ctor argument
        if isinstance(year_or_value, int):

            # If first argument is int, it may be year or ISO int for the entire date
            year_or_iso_int: int = year_or_value

            if 1970 <= year_or_iso_int <= 9999:

                # First argument is year if in the range from 1970 to 9999 (inclusive)
                year: int = year_or_iso_int

                # This is one type of input where remaning args are used
                remaining_args_must_be_none = False

                # If the first argument is year, month and day are required
                if month is None:
                    raise Exception(f'In LocalDate constructor, first argument {year} is year '
                                    f'in which case month must be specified.')
                if day is None:
                    raise Exception(f'In LocalDate constructor, first argument {year} is year '
                                    f'in which case day must be specified.')

                # Convert to int in ISO yyyymmdd format
                self.__iso_int = 10_000 * year + 100 * month + day

            elif 19700101 <= year_or_iso_int <= 99991231:

                # First argument is year in ISO yyyymmdd format
                self.__iso_int = year_or_iso_int

            else:
                raise Exception(f'First argument of LocalDate constructor {year_or_iso_int} is neither the year, '
                                f'nor the entire date as int in ISO yyyymmdd format.')

        elif isinstance(year_or_value, str):

            # If argument is a string, it must use ISO yyyy-mm-dd format without timezone
            iso_string: str = year_or_value

            # Convert from string in yyyy-mm-dd format
            date_from_str: dt.date = dt.date.fromisoformat(iso_string)

            # Convert to int in ISO yyyymmdd format
            self.__iso_int = 10_000 * date_from_str.year + 100 * date_from_str.month + date_from_str.day

        elif isinstance(year_or_value, dt.date):

            # First argument is dt.datetime
            date_arg: dt.date = year_or_value

            # Convert to int in ISO yyyymmdd format
            self.__iso_int = 10_000 * date_arg.year + 100 * date_arg.month + date_arg.day

        else:
            raise Exception(f'First argument of LocalDate constructor {year_or_value} must be one of '
                            f'(a) year, (b) integer in ISO yyyymmdd format, (c) string in ISO yyyy-mm-dd format, '
                            f'or (d) dt.date.')

        # Depending on what is passed as the first argument, validate the remaining arguments
        if remaining_args_must_be_none:

            # If the first argument is not year, the remaining arguments must be None
            if month is not None:
                raise Exception(f'In LocalDate constructor, first argument {year_or_value} is the entire date '
                                f'rather than year, in which case month={month} must be None.')
            if day is not None:
                raise Exception(f'In LocalDate constructor, first argument {year_or_value} is the entire date '
                                f'rather than year, in which case day={day} must be None.')

    def __str__(self) -> str:
        """Convert to string in ISO yyyy-mm-dd format."""
        # We could directly format the output to string, however
        # this step will check that it is a valid date
        d: dt.date = self.to_date()
        result: str = d.isoformat()
        return result

    def to_iso_int(self) -> int:
        """Convert to int in ISO yyyymmdd format."""
        return self.__iso_int

    def to_date(self) -> dt.date:
        """Convert to dt.date."""
        value: int = self.__iso_int
        year: int = value // 10_000
        value -= year * 10_000
        month: int = value // 100
        value -= month * 100
        day: int = value
        result: dt.date = dt.date(year, month, day)
        return result
