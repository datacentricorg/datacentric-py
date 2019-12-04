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

from datacentric.storage.class_info import ClassInfo
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.data import Data
from datacentric.testing.unit_test import UnitTest


class BaseRecord(TypedRecord):
    pass


class BaseKey(TypedKey[BaseRecord]):
    pass


class DerivedRecord(BaseRecord):
    pass


class ElementData(Data):
    pass


class TestClassInfo(unittest.TestCase, UnitTest):
    def test_root_type(self):
        with self.assertRaises(Exception):
            ClassInfo.get_root_type(TypedKey[BaseRecord])
        with self.assertRaises(Exception):
            ClassInfo.get_root_type(ClassInfo)
        self.assertTrue(ClassInfo.get_root_type(BaseKey) == BaseKey)
        self.assertTrue(ClassInfo.get_root_type(BaseRecord) == BaseRecord)
        self.assertTrue(ClassInfo.get_root_type(DerivedRecord) == BaseRecord)
        self.assertTrue(ClassInfo.get_root_type(ElementData) == ElementData)

    @unittest.skip('Remove')
    def test_key_type(self):
        self.assertEqual(ClassInfo.get_key_from_record(BaseRecord), BaseKey)
        self.assertEqual(ClassInfo.get_key_from_record(DerivedRecord), BaseKey)


if __name__ == "__main__":
    unittest.main()
