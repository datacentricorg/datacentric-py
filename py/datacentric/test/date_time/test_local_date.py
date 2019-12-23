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

import timeit
import random
import unittest
import datetime as dt

from typing import Union
from datacentric.date_time.local_date import LocalDate


class TestLocalDate(unittest.TestCase):
    """Unit tests for LocalDate."""

    def test_smoke(self):
        """Smoke test"""

        # Created dates t1-t5 must match this value of string and/or Unix millis
        date_str: str = '2003-05-01'
        iso_int: int = 20030501

        # Validation
        d1: int = LocalDate(iso_int)
        LocalDate.validate(d1)

        # Create from year, month, day
        d2: int = LocalDate.from_fields(2003, 5, 1)
        self.assertEqual(d2, iso_int)

        # Create from string
        d3: int = LocalDate.from_str(date_str)
        self.assertEqual(d3, iso_int)

        # Create from dt.date
        d: dt.date = dt.date.fromisoformat(date_str)
        d4: int = LocalDate.from_date(d)
        self.assertEqual(d4, iso_int)

        # Test conversion to dt.date
        self.assertEqual(LocalDate.to_date(d1), d)

        # Test string representation roundtrip
        self.assertEqual(LocalDate.to_str(d1), date_str)

    @unittest.skip('Performance')
    def test_perf(self):
        count = 1000
        repeat = 1000

        def gen_datetime(min_year=1970, max_year=dt.datetime.now().year):
            start = dt.datetime(min_year, 1, 1, 00, 00, 00)
            years = max_year - min_year + 1
            end = start + dt.timedelta(days=365 * years)
            return start + (end - start) * random.random()

        as_dates = [x.date() for x in [gen_datetime() for i in range(count)]]

        as_ints = [LocalDate.from_date(x) for x in as_dates]
        as_fields = [LocalDate.to_fields(x) for x in as_ints]
        as_str = [LocalDate.to_str(x) for x in as_ints]

        t = timeit.timeit('[LocalDate.to_date(x) for x in as_ints]',
                          globals={'LocalDate': LocalDate, 'as_ints': as_ints}, number=repeat)
        print(f'{t:.4f}: int->dt.date')

        t = timeit.timeit('[LocalDate.from_date(x) for x in as_dates]',
                          globals={'LocalDate': LocalDate, 'as_dates': as_dates}, number=repeat)
        print(f'{t:.4f}: date->int')
        print('===================')

        t = timeit.timeit('[LocalDate.to_fields(x) for x in as_ints]',
                          globals={'LocalDate': LocalDate, 'as_ints': as_ints}, number=repeat)
        print(f'{t:.4f}: int->Tuple[int, int, int]')
        t = timeit.timeit('[LocalDate.from_fields(x[0], x[1], x[2]) for x in as_fields]',
                          globals={'LocalDate': LocalDate, 'as_fields': as_fields}, number=repeat)
        print(f'{t:.4f}: Tuple[int, int, int]->int')
        print('===================')

        t = timeit.timeit('[LocalDate.to_str(x) for x in as_ints]',
                          globals={'LocalDate': LocalDate, 'as_ints': as_ints}, number=repeat)
        print(f'{t:.4f}: int->str')
        t = timeit.timeit('[LocalDate.from_str(x) for x in as_str]',
                          globals={'LocalDate': LocalDate, 'as_str': as_str}, number=repeat)
        print(f'{t:.4f}: str->int')
        print('===================')

        t = timeit.timeit('[LocalDate.validate(x) for x in as_ints]',
                          globals={'LocalDate': LocalDate, 'as_ints': as_ints}, number=repeat)
        print(f'{t:.4f}: validate')


if __name__ == "__main__":
    unittest.main()
