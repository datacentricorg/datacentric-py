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
from datacentric.date_time.local_date import LocalDate


class TestLocalDate(unittest.TestCase):
    """Unit tests for LocalDate."""

    def test_smoke(self):
        """Smoke test"""

        # Created dates t1-t5 must match this value of string and/or Unix millis
        date_str: str = '2003-05-01'
        iso_int: int = 20030501

        # Validation
        d1: Union[int, LocalDate] = LocalDate(iso_int)
        LocalDate.validate(d1)

        # Create from year, month, day
        d2: Union[int, LocalDate] = LocalDate.from_fields(2003, 5, 1)
        self.assertEqual(d2, iso_int)

        # Create from string
        d3: Union[int, LocalDate] = LocalDate.from_str(date_str)
        self.assertEqual(d3, iso_int)

        # Create from dt.date
        d: dt.date = dt.date.fromisoformat(date_str)
        d4: Union[int, LocalDate] = LocalDate.from_date(d)
        self.assertEqual(d4, iso_int)

        # Test conversion to dt.date
        self.assertEqual(LocalDate.to_date(d1), d)

        # Test string representation roundtrip
        self.assertEqual(LocalDate.to_str(d1), date_str)


if __name__ == "__main__":
    unittest.main()
