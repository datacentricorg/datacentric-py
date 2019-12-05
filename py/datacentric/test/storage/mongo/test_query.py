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
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.nullable_elements_sample import NullableElementsSample, NullableElementsSampleKey
from datacentric.storage.mongo.temporal_mongo_unit_test_context import TemporalMongoUnitTestContext
from datacentric.testing.unit_test import UnitTestKey, UnitTest


class TestQuery(unittest.TestCase, UnitTest):
    def test_nullable_elements(self):
        with TemporalMongoUnitTestContext(self) as context:

            for record_index in range(8):
                record_index_mod2 = record_index % 2
                record_index_mod4 = record_index % 4
                record = NullableElementsSample()
                # record.record_name = ['A', 'B'][record_index % 2]
                record.record_index = record_index
                record.data_set = context.data_set
                record.string_token = 'A' + str(record_index_mod4)
                record.bool_token = record_index_mod2 == 0
                record.int_token = record_index_mod4
                record.local_date_token = LocalDate.from_ints(2003, 5, 1 + record_index_mod4)
                record.local_time_token = LocalTime(10, 15, 30 + record_index_mod4).to_iso_int()
                record.local_minute_token = LocalMinute(10, record_index_mod4).to_iso_int()
                record.local_date_time_token = LocalDateTime(2003, 5, 1 + record_index_mod4, 10, 15).to_iso_int()
                record.enum_token = EnumSample(record_index_mod2 + 1)

                context.data_source.save_one(NullableElementsSample, record, context.data_set)

            query = context.data_source.get_query(NullableElementsSample, context.data_set)

            # Unconstrained query
            unconstrained_results = []
            for obj in query.as_iterable():  # type: NullableElementsSample
                unconstrained_results.append((obj.key, obj.record_index))

            expected = [('A0;true;0;20030501;101530000;1000;20030501101500000;EnumValue1', 4),
                        ('A1;false;1;20030502;101531000;1001;20030502101500000;EnumValue2', 5),
                        ('A2;true;2;20030503;101532000;1002;20030503101500000;EnumValue1', 6),
                        ('A3;false;3;20030504;101533000;1003;20030504101500000;EnumValue2', 7)]

            for expected_sample in expected:
                self.assertTrue(expected_sample in unconstrained_results)

            # Query with constraints
            query = context.data_source.get_query(NullableElementsSample, context.data_set) \
                .where({'string_token': 'A1'}).where({'bool_token': False}).where({'int_token': 1}) \
                .where({'local_date_token': LocalDate(2003, 5, 1 + 1)}) \
                .where({'local_time_token': LocalTime(10, 15, 30 + 1)}) \
                .where({'local_minute_token': LocalMinute(10, 1)}) \
                .where({'local_date_time_token': LocalDateTime(2003, 5, 1 + 1, 10, 15)}) \
                .where({'enum_token': EnumSample.EnumValue2})

            constrained_results = []
            for obj in query.as_iterable():
                constrained_results.append((obj.key, obj.record_index))

            expected_constrained = ('A1;false;1;20030502;101531000;1001;20030502101500000;EnumValue2', 5)
            self.assertTrue(expected_constrained in constrained_results)


if __name__ == "__main__":
    unittest.main()
