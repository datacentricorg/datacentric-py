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


class LocalDateTime(int, ABC):
    """
    Represents datetime to millisecond precision, with no reference to a
    particular time zone, and provides conversion to and from:

    * Integer year, month, day, hour, minute, second, and optional millisecond
    * Integer to millisecond precision in yyyymmddhhmmssfff format
    * ISO string to millisecond precision in yyyy-mm-ddThh:mm:ss.fff format;
      seconds always have 3 digits after the decimal point, irrespective
      of how many digits are actually required.
    * Python dt.time without timezone
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
    def from_fields(cls, year: int, month: int, day: int, hour: int = 0,
                    minute: int = 0, second: int = 0, millisecond: Optional[int] = None) -> Union[int, 'LocalDateTime']:
        """
        Convert hour to millisecond fields to LocalDateTime represented in yyyymmddhhmmssfff format.

        Millisecond field is optional. Zero value will be assumed if not specified.
        """

        # If millisecond is not specified, assume 0
        if millisecond is None:
            millisecond = 0

        # Convert to LocalDateTime represented in yyyymmddhhmmssfff format
        result: int = 1000_00_00_00_00_00 * year + 1000_00_00_00_00 * month + 1000_00_00_00 * day + \
                      1000_00_00 * hour + 1000_00 * minute + 1000 * second + millisecond

        # Validate and return
        cls.validate(result)
        return result

    @classmethod
    def validate(cls, value: Union[int, 'LocalDateTime']) -> None:
        """
        Raise exception if the argument is not None, and is not an
        int in yyyymmddhhmmssfff format.

        This fast validation method will not detect errors such as Feb 31.
        """

        # If None, return before doing other checks
        if value is None:
            return

        # Convert to tuple
        year, month, day, hour, minute, second, millisecond = cls.__to_fields_lenient(value)

        if not (1970 <= year <= 9999):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The year {year} should be in 1970 to 9999 range.')
        if not (1 <= month <= 12):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The month {month} should be in 1 to 12 range.')
        if not (1 <= day <= 31):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The day {day} should be in 1 to 31 range.')
        if not (0 <= hour <= 23):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The hour {hour} should be in 0 to 23 range.')
        if not (0 <= minute <= 59):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The minute {minute} should be in 0 to 59 range.')
        if not (0 <= second <= 59):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The second {second} should be in 0 to 59 range.')
        if not (0 <= millisecond <= 999):
            raise Exception(f'LocalDateTime {value} is not in yyyymmddhhmmssfff format. '
                            f'The millisecond {millisecond} should be in 0 to 999 range.')

    @classmethod
    def __to_fields_lenient(cls, value: Union[int, 'LocalDateTime']) -> Tuple[int, int, int, int, int, int, int]:
        """
        Convert LocalDateTime represented as int in yyyymmddhhmmssfff format to
        the tuple (year, month, day, hour, minute, second, millisecond).

        This method does not perform validation of its argument.
        """

        year: int = value // 1000_00_00_00_00_00
        value -= year * 1000_00_00_00_00_00
        month: int = value // 1000_00_00_00_00
        value -= month * 1000_00_00_00_00
        day: int = value // 1000_00_00_00
        value -= day * 1000_00_00_00
        hour: int = value // 1000_00_00
        value -= hour * 1000_00_00
        minute: int = value // 1000_00
        value -= minute * 1000_00
        second: int = value // 1000
        value -= second * 1000
        millisecond: int = value

        return year, month, day, hour, minute, second, millisecond
