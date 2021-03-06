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
from datacentric.storage.data_set import DataSet
from datacentric.storage.record import Record


class TestDataSet(unittest.TestCase):

    def test_key_instantiation(self):
        key = DataSet.create_key(data_set_name='key_id')
        self.assertTrue(key == 'DataSet=key_id')

    def test_abstract_fail(self):
        with self.assertRaises(TypeError):
            Record()


if __name__ == "__main__":
    unittest.main()
