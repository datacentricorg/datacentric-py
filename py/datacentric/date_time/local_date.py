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
from typing import Union, Tuple
import datetime as dt


class LocalDate(int, ABC):
    """
    Represents a date within the calendar, with no reference to a particular
    time zone or time of day, and provides conversion to and from:

    * Integer year, month, and day of month
    * ISO string in yyyy-mm-dd format
    * Python dt.date
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
    def from_fields(cls, year: int, month: int, day: int) -> Union[int, 'LocalDate']:
        """
        Convert year, month and day fields to LocalDate represented
        as int in yyyymmdd format.
        """

        # Convert to int in ISO yyyymmdd format
        result: int = 10_000 * year + 100 * month + day

        # Perform full validation and return
        cls.validate(result)
        return result

    @classmethod
    def to_fields(cls, value: Union[int, 'LocalDate']) -> Tuple[int, int, int]:
        """
        Convert LocalDate represented as int in yyyymmdd format.
        the tuple (year, month, day).
        """

        # Perform fast validation to detect values out of range.
        # This will not detect errors such as Feb 31
        cls.validate(value)

        # Convert to tuple
        year, month, day = cls.__to_fields_lenient(value)
        return year, month, day

    @classmethod
    def from_str(cls, iso_string: str) -> Union[int, 'LocalDate']:
        """
        Convert str in yyyy-mm-dd format to LocalDate represented
        as int in yyyymmdd format.
        """

        if iso_string.endswith('Z'):
            raise Exception(f'String {iso_string} passed to LocalDate ctor must not end with capital Z that '
                            f'indicates UTC timezone because LocalDate does not include timezone.')

        # Convert from string in yyyy-mm-dd format
        date_from_str: dt.date = dt.date.fromisoformat(iso_string)

        # Convert to int in ISO yyyymmdd format
        return 10_000 * date_from_str.year + 100 * date_from_str.month + date_from_str.day

    @classmethod
    def to_str(cls, value: Union[int, 'LocalDate']) -> str:
        """
        Convert LocalDate represented as int in yyyymmdd format
        to string in ISO yyyy-mm-dd format.
        """

        # Perform fast validation to detect values out of range.
        # This will not detect errors such as Feb 31
        cls.validate(value)

        # We could directly format the output to string, however
        # this step will check that it is a valid date
        d: dt.date = cls.to_date(value)
        result: str = d.isoformat()
        return result

    @classmethod
    def from_date(cls, date: dt.date) -> Union[int, 'LocalDate']:
        """Convert dt.date to LocalDate represented as int in yyyymmdd format."""
        return 10_000 * date.year + 100 * date.month + date.day

    @classmethod
    def to_date(cls, value: Union[int, 'LocalDate']) -> dt.date:
        """Convert LocalDate represented as int in yyyymmdd format to dt.date."""

        # Perform fast validation to detect values out of range.
        # This will not detect errors such as Feb 31
        cls.validate(value)

        # Convert to tuple
        year, month, day = cls.__to_fields_lenient(value)

        # This will also validate the date
        result: dt.date = dt.date(year, month, day)
        return result

    @classmethod
    def validate(cls, value: Union[int, 'LocalDate']) -> None:
        """
        Raise exception if the argument is not None and is not an int
        in yyyymmdd format.

        This fast validation method will not detect errors such as Feb 31.
        """

        # If None, return before doing other checks
        if value is None:
            return

        # Convert to tuple
        year, month, day = cls.__to_fields_lenient(value)

        if not (1970 <= year <= 9999):
            raise Exception(f'LocalDate {value} is not in readable yyyymmdd format. '
                            f'The year {year} should be in 1970 to 9999 range.')
        if not (1 <= month <= 12):
            raise Exception(f'LocalDate {value} is not in readable yyyymmdd format. '
                            f'The month {month} should be in 1 to 12 range.')
        if not (1 <= day <= 31):
            raise Exception(f'LocalDate {value} is not in readable yyyymmdd format. '
                            f'The day {day} should be in 1 to 31 range.')

    @classmethod
    def __to_fields_lenient(cls, value: Union[int, 'LocalDate']) -> Tuple[int, int, int]:
        """
        Convert LocalDate represented as int in yyyymmdd format to
        the tuple (year, month, day).
        """

        year: int = value // 10_000
        value -= year * 10_000
        month: int = value // 100
        value -= month * 100
        day: int = value

        return year, month, day
