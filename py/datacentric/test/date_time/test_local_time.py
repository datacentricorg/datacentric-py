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

import unittest
import datetime as dt
from typing import Union
from datacentric.date_time.local_time import LocalTime
from datacentric.testing.unit_test import UnitTest


class TestLocalTime(unittest.TestCase, UnitTest):
    """Unit tests for LocalTime."""

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid exception in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        # Created dates t1-t5 must match this value of string and/or Unix millis
        time_str: str = '10:15:30.500'
        iso_int: int = 101530500

        # Validate
        t1: Union[int, LocalTime] = iso_int
        LocalTime.validate(t1)

        # Create from year, month, day
        t2: Union[int, LocalTime] = LocalTime.from_fields(10, 15, 30, 500)
        self.assertEqual(t2, iso_int)

        # Create from string
        t3: Union[int, LocalTime] = LocalTime.from_str(time_str)
        self.assertEqual(t3, iso_int)

        # Create from dt.time
        t: dt.time = dt.time.fromisoformat('10:15:30.500')
        t4: Union[int, LocalTime] = LocalTime.from_time(t)
        self.assertEqual(t4, iso_int)

        # Test conversion to dt.date
        self.assertEqual(LocalTime.to_time(t1), t)

        # Test string representation roundtrip
        self.assertEqual(LocalTime.to_str(t1), time_str)
        t6_str = '10:15:30'
        t6_str_result = '10:15:30.000'
        self.assertEqual(LocalTime.to_str(LocalTime.from_str(t6_str)), t6_str_result)
        t7_str = '10:15:30.1'
        t7_str_result = '10:15:30.100'
        self.assertEqual(LocalTime.to_str(LocalTime.from_str(t7_str)), t7_str_result)
        t8_str = '10:15:30.12'
        t8_str_result = '10:15:30.120'
        self.assertEqual(LocalTime.to_str(LocalTime.from_str(t8_str)), t8_str_result)
        t9_str = '10:15:30.123'
        t9_str_result = '10:15:30.123'
        self.assertEqual(LocalTime.to_str(LocalTime.from_str(t9_str)), t9_str_result)

        # Test rounding to the whole millisecond
        t10_str = '10:15:30.1234'
        t10_str_rounded = '10:15:30.123'
        self.assertEqual(LocalTime.to_str(LocalTime.from_str(t10_str)), t10_str_rounded)

if __name__ == "__main__":
    unittest.main()
