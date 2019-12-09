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
from datacentric.date_time.local_minute import LocalMinute


class TestLocalMinute(unittest.TestCase):
    """Unit tests for LocalMinute."""

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid exception in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        # Created minutes t1-t5 must match this value of string and/or Unix millis
        time_str: str = '10:15'
        iso_int: int = 1015

        # Validate
        t1: Union[int, LocalMinute] = iso_int
        LocalMinute.validate(t1)

        # Create from year, month, day
        t2: Union[int, LocalMinute] = LocalMinute.from_fields(10, 15)
        self.assertEqual(t2, iso_int)

        # Create from string
        t3: Union[int, LocalMinute] = LocalMinute.from_str(time_str)
        self.assertEqual(t3, iso_int)

        # Create from dt.time
        t: dt.time = dt.time.fromisoformat('10:15')
        t4: Union[int, LocalMinute] = LocalMinute.from_time(t)
        self.assertEqual(t4, iso_int)

        # Test conversion to dt.date
        self.assertEqual(LocalMinute.to_time(t1), t)

        # Test string representation roundtrip
        self.assertEqual(LocalMinute.to_str(t1), time_str)
        t6_str = '10:15'
        self.assertEqual(LocalMinute.to_str(LocalMinute.from_str(t6_str)), t6_str)

if __name__ == "__main__":
    unittest.main()
