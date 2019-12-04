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
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.test.storage.data_sample import BaseSampleKey
from datacentric.testing.unit_test import UnitTestKey, UnitTest


@attr.s(slots=True, auto_attribs=True)
class CompositeKeySampleKey(TypedKey['CompositeKeySample']):
    key_element1: str = attr.ib(default=None, kw_only=True)
    key_element2: BaseSampleKey = attr.ib(default=None, kw_only=True)
    key_element3: str = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class CompositeKeySample(TypedRecord[CompositeKeySampleKey]):
    key_element1: str = attr.ib(default=None, kw_only=True)
    key_element2: BaseSampleKey = attr.ib(default=None, kw_only=True)
    key_element3: str = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class SingletonSampleKey(TypedKey['SingletonSample']):
    pass


@attr.s(slots=True, auto_attribs=True)
class SingletonSample(TypedRecord[SingletonSampleKey]):
    string_element: str = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class IdBasedKeySampleKey(TypedKey['IdBasedKeySample']):
    id_: ObjectId = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class IdBasedKeySample(TypedRecord[IdBasedKeySampleKey]):
    string_element: str = attr.ib(default=None, kw_only=True)


class TestMongoKey(unittest.TestCase, UnitTest):
    def test_composite_key(self):
        rec = CompositeKeySample()
        rec.key_element1 = 'abc'
        rec.key_element2 = BaseSampleKey()
        rec.key_element2.record_id = 'def'
        rec.key_element2.record_index = 123
        rec.key_element3 = 'xyz'
        key_value = rec.to_key().value

        key = CompositeKeySampleKey()
        key.populate_from_string(key_value)
        self.assertEqual(key.key_element1, rec.key_element1)
        self.assertEqual(key.key_element2.record_id, rec.key_element2.record_id)
        self.assertEqual(key.key_element2.record_index, rec.key_element2.record_index)
        self.assertEqual(key.key_element3, rec.key_element3)

    def test_singleton_key(self):
        rec = SingletonSample()
        rec.string_element = 'abc'

        key_value = rec.to_key().value
        self.assertEqual(key_value, '')

        key = SingletonSampleKey()
        key.populate_from_string(key_value)
        self.assertEqual(key.value, key_value)

    def test_id_based_key(self):
        rec = IdBasedKeySample()
        rec.id_ = ObjectId.from_datetime(dt.datetime.fromtimestamp(123456789))
        rec.string_element = 'abc'

        key_value = rec.to_key().value
        key = IdBasedKeySampleKey()
        key.populate_from_string(key_value)
        self.assertEqual(key_value, str(key))


if __name__ == "__main__":
    unittest.main()
