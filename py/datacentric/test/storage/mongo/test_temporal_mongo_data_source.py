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
from bson import ObjectId
from datacentric.storage.context import Context
from datacentric.storage.data_set import DataSet
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.element_sample import ElementSample
from datacentric.test.storage.base_sample import BaseSample, BaseSampleKey
from datacentric.test.storage.derived_sample import DerivedSample
from datacentric.storage.mongo.temporal_mongo_unit_test_context import TemporalMongoUnitTestContext
from datacentric.testing.unit_test import UnitTestKey, UnitTest


def save_base_record(context: Context, data_set_id, record_id, record_index) -> ObjectId:
    rec = BaseSample()
    rec.record_name = record_id
    rec.record_index = record_index
    rec.double_element = 100.0
    rec.local_date_element = LocalDate.from_fields(2003, 5, 1)
    rec.local_time_element = LocalTime.from_fields(10, 15, 30)  # 10:15:30
    rec.local_minute_element = LocalMinute.from_fields(10, 15)  # 10:15
    rec.local_date_time_element = LocalDateTime.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
    rec.enum_value = EnumSample.EnumValue2

    data_set = context.data_source.get_data_set(data_set_id, context.data_set)
    context.data_source.save_one(BaseSample, rec, data_set)

    return rec.id_


def save_derived_record(context, data_set_id, record_id, record_index) -> ObjectId:
    rec = DerivedSample()
    rec.record_name = record_id
    rec.record_index = record_index
    rec.double_element = 300.
    rec.local_date_element = LocalDate.from_fields(2003, 5, 1)
    rec.local_time_element = LocalTime.from_fields(10, 15, 30)  # 10:15:30
    rec.local_minute_element = LocalMinute.from_fields(10, 15)  # 10:15
    rec.local_date_time_element = LocalDateTime.from_fields(2003, 5, 1, 10, 15)  # 2003-05-01T10:15:00
    rec.string_element2 = ''
    rec.double_element = 200.
    rec.list_of_string = ['A', 'B', 'C']

    rec.list_of_double = [1.0, 2.0, 3.0]
    rec.list_of_nullable_double = [10.0, None, 30.0]

    # Data element
    rec.data_element = ElementSample()
    rec.data_element.double_element3 = 1.0
    rec.data_element.string_element3 = 'AA'

    # Data element list

    element_list0 = ElementSample()
    element_list0.double_element3 = 1.0
    element_list0.string_element3 = "A0"
    element_list1 = ElementSample()
    element_list1.double_element3 = 2.0
    element_list1.string_element3 = "A1"
    rec.data_element_list = [element_list0, element_list1]

    # Key element
    rec.key_element = 'BB;2'

    # Key element list
    rec.key_element_list = ['B0;3', 'B1;4']

    data_set = context.data_source.get_data_set(data_set_id, context.data_set)
    context.data_source.save_one(DerivedSample, rec, data_set)
    return rec.id_


def save_basic_data(context: Context):
    data_set0 = context.data_source.create_data_set('DataSet0', context.data_set)
    save_base_record(context, 'DataSet0', 'A', 0)
    context.data_source.create_data_set('DataSet1', context.data_set, [data_set0])
    save_derived_record(context, 'DataSet1', 'B', 0)


def verify_load(context, data_set_id, key):
    data_set = context.data_source.get_data_set(data_set_id, context.data_set)
    record = context.data_source.load_or_null_by_key(BaseSample, key, data_set)
    if record is None:
        return 'Not found'
    else:
        if record.to_key() != key:
            return 'Found, key mismatch.'
        else:
            return f'Found, type = {type(record).__name__}'


def save_minimal_record(context, data_set_id, record_id, record_index, version):
    rec = BaseSample()
    rec.record_name = record_id
    rec.record_index = record_index
    rec.version = version

    data_set = context.data_source.get_data_set(data_set_id, context.data_set)
    context.data_source.save_one(BaseSample, rec, data_set)

    return rec.id_


class TestTemporalMongoDataSource(unittest.TestCase, UnitTest):
    """Tests for the temporal data source."""

    def test_smoke(self):
        """Smoke test."""

        with TemporalMongoUnitTestContext() as context:
            save_basic_data(context)

            key_a0 = 'BaseSample=A;0'
            key_b0 = 'BaseSample=B;0'

            self.assertEqual('Found, type = BaseSample', verify_load(context, 'DataSet0', key_a0))
            self.assertEqual('Found, type = BaseSample', verify_load(context, 'DataSet1', key_a0))
            self.assertEqual('Not found', verify_load(context, 'DataSet0', key_b0))
            self.assertEqual('Found, type = DerivedSample', verify_load(context, 'DataSet1', key_b0))

    def test_multiple_data_set_query(self):
        with TemporalMongoUnitTestContext() as context:
            # Begin from DataSet0
            data_set0 = context.data_source.create_data_set('DataSet0', context.data_set)

            # Create initial version of the records
            save_minimal_record(context, 'DataSet0', 'A', 0, 0)
            save_minimal_record(context, 'DataSet0', 'B', 1, 0)
            save_minimal_record(context, 'DataSet0', 'A', 2, 0)
            save_minimal_record(context, 'DataSet0', 'B', 3, 0)

            # Create second version of some records
            save_minimal_record(context, 'DataSet0', 'A', 0, 1)
            save_minimal_record(context, 'DataSet0', 'B', 1, 1)
            save_minimal_record(context, 'DataSet0', 'A', 2, 1)
            save_minimal_record(context, 'DataSet0', 'B', 3, 1)

            # Create third version of even fewer records
            save_minimal_record(context, 'DataSet0', 'A', 0, 2)
            save_minimal_record(context, 'DataSet0', 'B', 1, 2)
            save_minimal_record(context, 'DataSet0', 'A', 2, 2)
            save_minimal_record(context, 'DataSet0', 'B', 3, 2)

            # Same in DataSet1
            data_set1 = context.data_source.create_data_set("DataSet1", context.data_set, [data_set0])

            # Create initial version of the records
            save_minimal_record(context, "DataSet1", "A", 4, 0)
            save_minimal_record(context, "DataSet1", "B", 5, 0)
            save_minimal_record(context, "DataSet1", "A", 6, 0)
            save_minimal_record(context, "DataSet1", "B", 7, 0)

            # Create second version of some records
            save_minimal_record(context, "DataSet1", "A", 4, 1)
            save_minimal_record(context, "DataSet1", "B", 5, 1)
            save_minimal_record(context, "DataSet1", "A", 6, 1)
            save_minimal_record(context, "DataSet1", "B", 7, 1)

            # Next in DataSet2
            data_set2 = context.data_source.create_data_set("DataSet2", context.data_set, [data_set0])
            save_minimal_record(context, "DataSet2", "A", 8, 0)
            save_minimal_record(context, "DataSet2", "B", 9, 0)

            # Next in DataSet3
            data_set3 = context.data_source.create_data_set("DataSet3", context.data_set,
                                                            [data_set0, data_set1, data_set2])
            save_minimal_record(context, "DataSet3", "A", 10, 0)
            save_minimal_record(context, "DataSet3", "B", 11, 0)

            query = context.data_source.get_query(BaseSample, data_set3) \
                .where({'record_name': 'B'}) \
                .sort_by('record_name') \
                .sort_by('record_index')

            query_result = []
            for obj in query.as_iterable():  # type: BaseSample
                data_set: DataSet = context.data_source.load_or_null(DataSet, obj.data_set)
                data_set_name = data_set.data_set_name
                query_result.append((obj.to_key().split('=', 1)[1], data_set_name, obj.version))

            self.assertEqual(query_result[0], ('B;1', 'DataSet0', 2))
            self.assertEqual(query_result[1], ('B;3', 'DataSet0', 2))
            self.assertEqual(query_result[2], ('B;5', 'DataSet1', 1))
            self.assertEqual(query_result[3], ('B;7', 'DataSet1', 1))
            self.assertEqual(query_result[4], ('B;9', 'DataSet2', 0))
            self.assertEqual(query_result[5], ('B;11', 'DataSet3', 0))

    def test_create_ordered_id(self):
        """Stress tests to check ObjectIds are created in increasing order."""
        with TemporalMongoUnitTestContext() as context:
            for i in range(10_000):
                context.data_source.create_ordered_object_id()

            # Log should not contain warnings.
            # TODO: fix logging
            # self.assertTrue(str(context.log) == '')


if __name__ == "__main__":
    unittest.main()
