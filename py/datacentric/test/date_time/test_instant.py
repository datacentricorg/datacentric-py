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

        # Created dates t1-t5 must match this value of Unix millis
        unix_millis: int = 1051784130500

        # Create from milliseconds since Unix epoch
        t1: Instant = Instant(unix_millis)
        self.assertEqual(t1.to_unix_millis(), unix_millis)

        # Create from year, month, etc.
        t2: Instant = Instant(2003, 5, 1, 10, 15, 30, 500)
        self.assertEqual(t2.to_unix_millis(), unix_millis)

        # Create from string
        t3: Instant = Instant('2003-05-01T10:15:30.500Z')
        self.assertEqual(t3.to_unix_millis(), unix_millis)

        # Create from dt.datetime
        dtime: dt.datetime = dateutil.parser.parse('2003-05-01T10:15:30.500Z')
        t4: Instant = Instant(dtime)
        self.assertEqual(t4.to_unix_millis(), unix_millis)

        # Create from pd.timestamp
        tstamp: pd.Timestamp = pd.Timestamp('2003-05-01T10:15:30.500Z')
        t5: Instant = Instant(tstamp)
        self.assertEqual(t5.to_unix_millis(), unix_millis)

        # Test conversion to dt.datetime
        self.assertEqual(t1.to_datetime(), dtime)


if __name__ == "__main__":
    unittest.main()
