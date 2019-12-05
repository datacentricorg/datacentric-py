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
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.test.storage.base_sample_key import BaseSampleKey
from datacentric.test.storage.base_sample import BaseSample
from datacentric.test.storage.composite_key_sample_key import CompositeKeySampleKey
from datacentric.test.storage.composite_key_sample import CompositeKeySample
from datacentric.test.storage.singleton_sample_key import SingletonSampleKey
from datacentric.test.storage.singleton_sample import SingletonSample
from datacentric.test.storage.id_based_key_sample_key import IdBasedKeySampleKey
from datacentric.test.storage.id_based_key_sample import IdBasedKeySample
from datacentric.testing.unit_test import UnitTestKey, UnitTest


class TestMongoKey(unittest.TestCase, UnitTest):
    """Test for key generation."""

    def test_composite_key(self):
        """Test generation of composite key."""

        # From record
        rec = CompositeKeySample()
        rec.key_element1 = 'abc'
        rec.key_element2 = BaseSample.create_key(record_id='def', record_index=123)
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


if __name__ == "__main__":
    unittest.main()
