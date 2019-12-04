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
from datacentric.storage.data_set import DataSetKey
from datacentric.storage.record import Record
from datacentric.testing.unit_test import UnitTestKey, UnitTest


class TestDataSet(unittest.TestCase, UnitTest):
    @unittest.skip
    def test_key_instantiation(self):
        null_key = DataSetKey()
        key = DataSetKey()
        key.data_set_name = 'key_id'
        self.assertTrue(null_key.data_set_name is None)
        self.assertTrue(key.data_set_name == 'key_id')

    def test_abstract_fail(self):
        with self.assertRaises(TypeError):
            Record()


if __name__ == "__main__":
    unittest.main()
