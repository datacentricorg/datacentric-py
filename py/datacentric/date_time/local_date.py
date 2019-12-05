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
from typing import Union
import datetime as dt


class LocalDate(int, ABC):
    """
    Represents a date within the calendar, with no reference to a particular
    time zone or time of day, and provides conversion to and from:

    * Integer year, month, and day of month
    * ISO string in yyyy-mm-dd format
    * Python dt.date
    """

    @staticmethod
    def to_iso_str(iso_int: int) -> str:
        """Convert to string in ISO yyyy-mm-dd format."""
        # We could directly format the output to string, however
        # this step will check that it is a valid date
        d: dt.date = LocalDate.to_date(iso_int)
        result: str = d.isoformat()
        return result

    @staticmethod
    def to_date(iso_int: int) -> dt.date:
        """Convert to dt.date."""
        value: int = iso_int
        year: int = value // 10_000
        value -= year * 10_000
        month: int = value // 100
        value -= month * 100
        day: int = value
        result: dt.date = dt.date(year, month, day)
        return result

    @staticmethod
    def from_date(date: dt.date) -> Union[int, 'LocalDate']:
        """Convert to int in ISO yyyymmdd format."""
        return 10_000 * date.year + 100 * date.month + date.day

    @staticmethod
    def from_iso_str(iso_string: str) -> Union[int, 'LocalDate']:
        """Convert from str in yyyy-mm-dd format to int in ISO yyyymmdd format."""
        if iso_string.endswith('Z'):
            raise Exception(f'String {iso_string} passed to LocalDate ctor must not end with capital Z that '
                            f'indicates UTC timezone because LocalDate does not include timezone.')

        # Convert from string in yyyy-mm-dd format
        date_from_str: dt.date = dt.date.fromisoformat(iso_string)

        # Convert to int in ISO yyyymmdd format
        return 10_000 * date_from_str.year + 100 * date_from_str.month + date_from_str.day

    @staticmethod
    def from_ints(year: int, month: int, day: int) -> Union[int, 'LocalDate']:
        """Convert int year, month and day to readable int format."""

        # TODO: improve check
        if not (1970 <= year <= 9999):
            raise Exception(f'year should be in 1970..9999 range.')
        if not (1 <= month <= 12):
            raise Exception(f'month should be in 1..12 range.')
        if not (1 <= month <= 31):
            raise Exception(f'day should be in 1..31 range.')

        # Convert to int in ISO yyyymmdd format
        return 10_000 * year + 100 * month + day

    @abstractmethod
    def abstract_class_guard(self) -> None:
        """
        Guard method to prevent this abstract base class from
        being instantiated.
        """
        pass
