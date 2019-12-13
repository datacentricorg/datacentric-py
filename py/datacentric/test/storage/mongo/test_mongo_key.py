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

import attr
import unittest
import datetime as dt
from bson import ObjectId
import datacentric as dc
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.base_sample import BaseSample
from datacentric.test.storage.composite_key_sample import CompositeKeySample
from datacentric.test.storage.singleton_sample import SingletonSample
from datacentric.test.storage.id_based_key_sample import IdBasedKeySample
from datacentric.test.storage.nullable_elements_sample import NullableElementsSample


class TestMongoKey(unittest.TestCase):
    """Test for key generation."""

    def test_composite_key(self):
        """Test generation of composite key."""

        # From record
        rec = CompositeKeySample()
        rec.key_element1 = 'abc'
        rec.key_element2 = BaseSample.create_key(record_name='def', record_index=123)
        rec.key_element3 = 'xyz'
        key1 = rec.to_key()
        self.assertEqual(key1, 'CompositeKeySample=abc;def;123;xyz')

        # Using static method
        key2 = CompositeKeySample.create_key(key_element1=rec.key_element1, key_element2=rec.key_element2, key_element3=rec.key_element3)
        self.assertEqual(key2, 'CompositeKeySample=abc;def;123;xyz')

    def test_singleton_key(self):
        """Test singleton key generation."""

        # From record
        rec = SingletonSample()
        rec.string_element = 'abc'
        key1 = rec.to_key()
        self.assertEqual(key1, 'SingletonSample=')

        # Using static method
        key2 = SingletonSample.create_key()
        self.assertEqual(key2, 'SingletonSample=')

    def test_id_based_key(self):
        """Test ID-based key generation."""

        # From record
        rec = IdBasedKeySample()
        rec.id_ = ObjectId.from_datetime(dt.datetime.fromtimestamp(123456789))
        key1 = rec.to_key()
        self.assertEqual(key1, 'IdBasedKeySample=' + str(rec.id_))

        # Using static method
        key1 = rec.to_key()
        key2 = IdBasedKeySample.create_key(id_=rec.id_)
        self.assertEqual(key2, 'IdBasedKeySample=' + str(rec.id_))

    def test_nullable_elements_key(self):
        """Test generation of key consisting of nullable elements."""

        # Create key from nullable elements
        key = NullableElementsSample.create_key(
            string_token='ABC',
            bool_token=True,
            int_token=123,
            long_token=1234567890,
            local_date_token=dc.LocalDate.from_fields(2017, 7, 14),
            local_time_token=dc.LocalTime.from_fields(10, 15, 30, 500),
            local_minute_token=dc.LocalMinute.from_fields(10, 15),
            local_date_time_token=dc.LocalDateTime.from_fields(2017, 7, 14, 10, 15, 30, 500),
            instant_token=dc.Instant.from_fields(2017, 7, 14, 10, 15, 30, 500),
            enum_token=EnumSample.EnumValue1)
        self.assertEqual(key, 'NullableElementsSample=ABC;true;123;1234567890;20170714;101530500;1015;20170714101530500;2017-07-14T10:15:30.500Z;EnumValue1')

if __name__ == "__main__":
    unittest.main()
