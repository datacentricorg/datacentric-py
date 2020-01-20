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
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.date_time.instant import Instant
from datacentric.test.storage.date_sample import DatesSample
from datacentric.storage.mongo.temporal_mongo_unit_test_context import TemporalMongoUnitTestContext


class TestDateRoundTrip(unittest.TestCase):
    """Tests for TestDateRoundTrip."""

    def test_smoke(self):
        """Smoke test to check equality after data source save/load."""

        with TemporalMongoUnitTestContext() as context:
            data_set0 = context.data_source.create_data_set('DataSet0')

            rec = DatesSample()
            rec.record_name = 'Sample'
            rec.local_date_element = LocalDate.from_fields(2003, 5, 1)
            rec.local_time_element = LocalTime.from_fields(10, 15, 30)  # 10:15:30
            rec.local_minute_element = LocalMinute.from_fields(10, 15)  # 10:15
            rec.local_date_time_element = LocalDateTime.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
            rec.instant_element = Instant.from_fields(2003, 5, 1, 10, 15, 0)

            rec.date_element = dt.date(2003, 5, 1)
            rec.time_element = dt.time(10, 15, 30)
            rec.date_time_element = dt.datetime(2003, 5, 1, 10, 15)

            context.data_source.save_one(DatesSample, rec, data_set0)

            loaded = context.data_source.load_by_key(DatesSample, rec.to_key(), data_set0)

            self.assertEqual(rec.record_name, loaded.record_name)
            self.assertEqual(rec.local_minute_element, loaded.local_minute_element)
            self.assertEqual(rec.local_date_element, loaded.local_date_element)
            self.assertEqual(rec.local_time_element, loaded.local_time_element)
            self.assertEqual(rec.local_date_time_element, loaded.local_date_time_element)
            self.assertEqual(rec.instant_element, loaded.instant_element)

            self.assertEqual(rec.date_element, loaded.date_element)
            self.assertEqual(rec.time_element, loaded.time_element)
            self.assertEqual(rec.date_time_element, loaded.date_time_element)
