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
from typing import Union
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
        date_str: str = '2003-05-01T10:15:30.500Z'
        unix_millis: int = 1051784130500

        # Create from milliseconds since Unix epoch
        t1: Union[dt.datetime, Instant] = Instant.from_unix_millis(unix_millis)
        self.assertEqual(Instant.to_unix_millis(t1), unix_millis)

        # Create from year, month, etc.
        t2: Union[dt.datetime, Instant] = Instant.from_fields(2003, 5, 1, 10, 15, 30, 500)
        self.assertEqual(Instant.to_unix_millis(t2), unix_millis)

        # Create from string
        t3: Union[dt.datetime, Instant] = Instant.from_str(date_str)
        self.assertEqual(Instant.to_unix_millis(t3), unix_millis)

        # Create from dt.datetime constructed externally
        dtime: dt.datetime = dateutil.parser.parse(date_str)
        t4: Union[dt.datetime, Instant] = dtime
        self.assertEqual(Instant.to_unix_millis(t4), unix_millis)

        # Create from pd.timestamp constructed externally
        tstamp: pd.Timestamp = pd.Timestamp(date_str)
        t5: Union[dt.datetime, Instant] = tstamp.to_pydatetime()
        self.assertEqual(Instant.to_unix_millis(t5), unix_millis)

        # Test string representation conversion
        self.assertEqual(Instant.to_str(t1), date_str)
        t6_str = '2003-05-01T10:15:30Z'
        t6_str_result = '2003-05-01T10:15:30.000Z'
        self.assertEqual(Instant.to_str(Instant.from_str(t6_str)), t6_str_result)
        t7_str = '2003-05-01T10:15:30.1Z'
        t7_str_result = '2003-05-01T10:15:30.100Z'
        self.assertEqual(Instant.to_str(Instant.from_str(t7_str)), t7_str_result)
        t8_str = '2003-05-01T10:15:30.12Z'
        t8_str_result = '2003-05-01T10:15:30.120Z'
        self.assertEqual(Instant.to_str(Instant.from_str(t8_str)), t8_str_result)
        t9_str = '2003-05-01T10:15:30.123Z'
        t9_str_result = '2003-05-01T10:15:30.123Z'
        self.assertEqual(Instant.to_str(Instant.from_str(t9_str)), t9_str_result)

        # Test rounding to the whole millisecond
        t10_str = '2003-05-01T10:15:30.1234Z'
        t10_str_rounded = '2003-05-01T10:15:30.123Z'
        self.assertEqual(Instant.to_str(Instant.from_str(t10_str)), t10_str_rounded)


if __name__ == "__main__":
    unittest.main()
