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
from datacentric.testing.unit_test import UnitTest
from datacentric.date_time.local_minute import LocalMinute
from datacentric.testing.unit_test import UnitTestKey, UnitTest


class TestLocalMinute(unittest.TestCase, UnitTest):
    """Unit tests for LocalMinute."""

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid AttributeError in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        t = LocalMinute(12, 10)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 10)
        self.assertEqual(t.minute_of_day, 730)

        t1 = LocalMinute(12, 10)
        t2 = LocalMinute(1, 15)
        self.assertEqual(str(t1), '12:10')
        self.assertEqual(str(t2), '01:15')
        self.assertEqual(t1.to_time(), dt.time(12, 10))
        self.assertEqual(t2.to_time(), dt.time(1, 15))

        t = LocalMinute(12, 0)
        t1 = LocalMinute(12, 0)
        t2 = LocalMinute(13, 1)
        t3 = LocalMinute(14, 2)

        self.assertTrue(t1 == t)
        self.assertTrue(t1 != t2)
        self.assertTrue(t2 != t3)

        self.assertTrue(t1 <= t1)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t2 <= t3)

        self.assertTrue(t1 < t2)
        self.assertTrue(t1 < t3)
        self.assertTrue(t2 < t3)

        self.assertTrue(t1 >= t1)
        self.assertTrue(t2 >= t1)
        self.assertTrue(t3 >= t2)

        self.assertTrue(t2 > t1)
        self.assertTrue(t3 > t1)
        self.assertTrue(t3 > t2)


if __name__ == "__main__":
    unittest.main()
