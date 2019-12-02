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
from datacentric.date_time.local_date import LocalDate
from datacentric.testing.unit_test import UnitTest


class TestLocalDate(unittest.TestCase, UnitTest):
    """Unit tests for LocalDate."""

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid exception in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        # Created dates t1-t5 must match this value of string and/or Unix millis
        date_str: str = '2003-05-01'
        iso_int: int = 20030501

        # Create from milliseconds since Unix epoch
        d1: LocalDate = LocalDate(iso_int)
        self.assertEqual(d1.to_iso_int(), iso_int)

        # Create from year, month, day
        d2: LocalDate = LocalDate(2003, 5, 1)
        self.assertEqual(d2.to_iso_int(), iso_int)

        # Create from string
        d3: LocalDate = LocalDate(date_str)
        self.assertEqual(d3.to_iso_int(), iso_int)

        # Create from dt.date
        d: dt.date = dt.date.fromisoformat(date_str)
        d4: LocalDate = LocalDate(d)
        self.assertEqual(d4.to_iso_int(), iso_int)

        # Test conversion to dt.date
        self.assertEqual(d1.to_date(), d)

        # Test string representation roundtrip
        self.assertEqual(str(d1), date_str)


if __name__ == "__main__":
    unittest.main()
