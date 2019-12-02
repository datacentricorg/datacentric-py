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
from datacentric.date_time.instant import Instant
from datacentric.testing.unit_test import UnitTest


class TestInstant(unittest.TestCase, UnitTest):
    """Unit tests for Instant."""

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid exception in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        # Created dates t1-t5 must match this value of string and/or Unix millis
        date_str: str = '2003-05-01T10:15:30.5Z'
        unix_millis: int = 1051784130500

        # Create from milliseconds since Unix epoch
        t1: Instant = Instant(unix_millis)
        self.assertEqual(t1.to_unix_millis(), unix_millis)

        # Create from year, month, etc.
        t2: Instant = Instant(2003, 5, 1, 10, 15, 30, 500)
        self.assertEqual(t2.to_unix_millis(), unix_millis)

        # Create from string
        t3: Instant = Instant(date_str)
        self.assertEqual(t3.to_unix_millis(), unix_millis)

        # Create from dt.datetime
        dtime: dt.datetime = dateutil.parser.parse(date_str)
        t4: Instant = Instant(dtime)
        self.assertEqual(t4.to_unix_millis(), unix_millis)

        # Create from pd.timestamp
        tstamp: pd.Timestamp = pd.Timestamp(date_str)
        t5: Instant = Instant(tstamp)
        self.assertEqual(t5.to_unix_millis(), unix_millis)

        # Test conversion to dt.datetime
        self.assertEqual(t1.to_datetime(), dtime)

        # Test string representation roundtrip
        self.assertEqual(str(t1), date_str)
        t6_str = '2003-05-01T10:15:30Z'
        self.assertEqual(str(Instant(t6_str)), t6_str)
        t7_str = '2003-05-01T10:15:30.1Z'
        self.assertEqual(str(Instant(t7_str)), t7_str)
        t8_str = '2003-05-01T10:15:30.12Z'
        self.assertEqual(str(Instant(t8_str)), t8_str)
        t9_str = '2003-05-01T10:15:30.123Z'
        self.assertEqual(str(Instant(t9_str)), t9_str)

        # Test rounding to the whole millisecond
        t10_str = '2003-05-01T10:15:30.1234Z'
        t10_str_rounded = '2003-05-01T10:15:30.123Z'
        self.assertEqual(str(Instant(t10_str)), t10_str_rounded)

        # Check comparison operators
        t11a = Instant('2003-05-01T10:15:30.1Z')
        t11a_new_instance = Instant('2003-05-01T10:15:30.1Z')
        t11b = Instant('2003-05-01T10:15:30.12Z')
        self.assertTrue(t11a == t11a)
        self.assertTrue(t11a == t11a_new_instance)
        self.assertTrue(t11a != t11b)
        self.assertTrue(t11a <= t11a)
        self.assertTrue(t11a <= t11a_new_instance)
        self.assertTrue(t11a >= t11a)
        self.assertTrue(t11a >= t11a_new_instance)
        self.assertTrue(t11a < t11b)
        self.assertTrue(t11a <= t11b)
        self.assertTrue(t11b > t11a)
        self.assertTrue(t11b >= t11a)


if __name__ == "__main__":
    unittest.main()
