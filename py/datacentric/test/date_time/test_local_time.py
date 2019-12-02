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
import pandas as pd
import dateutil
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
        time_str: str = '10:15:30.5'
        iso_int: int = 101530500

        # Create from milliseconds since Unix epoch
        t1: LocalTime = LocalTime(iso_int)
        self.assertEqual(t1.to_iso_int(), iso_int)

        # Create from year, month, day
        t2: LocalTime = LocalTime(10, 15, 30, 500)
        self.assertEqual(t2.to_iso_int(), iso_int)

        # Create from string
        t3: LocalTime = LocalTime(time_str)
        self.assertEqual(t3.to_iso_int(), iso_int)

        # Create from dt.time
        t: dt.time = dt.time.fromisoformat('10:15:30.500')
        t4: LocalTime = LocalTime(t)
        self.assertEqual(t4.to_iso_int(), iso_int)

        # Test conversion to dt.date
        self.assertEqual(t1.to_time(), t)

        # Test string representation roundtrip
        self.assertEqual(str(t1), time_str)
        t6_str = '10:15:30'
        self.assertEqual(str(LocalTime(t6_str)), t6_str)
        t7_str = '10:15:30.1'
        self.assertEqual(str(LocalTime(t7_str)), t7_str)
        t8_str = '10:15:30.12'
        self.assertEqual(str(LocalTime(t8_str)), t8_str)
        t9_str = '10:15:30.123'
        self.assertEqual(str(LocalTime(t9_str)), t9_str)

        # Test rounding to the whole millisecond
        t10_str = '10:15:30.1234'
        t10_str_rounded = '10:15:30.123'
        self.assertEqual(str(LocalTime(t10_str)), t10_str_rounded)


if __name__ == "__main__":
    unittest.main()
