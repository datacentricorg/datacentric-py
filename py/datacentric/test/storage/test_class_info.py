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
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.storage.data import Data
from datacentric.test.storage.base_sample import BaseSample
from datacentric.test.storage.base_sample_key import BaseSampleKey
from datacentric.test.storage.derived_sample import DerivedSample
from datacentric.test.storage.element_sample import ElementSample
from datacentric.test.storage.root_sample import RootSample


class TestClassInfo(unittest.TestCase):
    """Tests for ClassInfo."""

    def smoke(self):
        """Smoke test."""

        with self.assertRaises(Exception):
            ClassInfo.get_ultimate_base(BaseSampleKey)
        with self.assertRaises(Exception):
            ClassInfo.get_ultimate_base(ClassInfo)
        self.assertTrue(ClassInfo.get_ultimate_base(BaseSample) == BaseSample)
        self.assertTrue(ClassInfo.get_ultimate_base(DerivedSample) == BaseSample)
        self.assertTrue(ClassInfo.get_ultimate_base(ElementSample) == ElementSample)
        self.assertTrue(ClassInfo.get_ultimate_base(RootSample) == RootSample)


if __name__ == "__main__":
    unittest.main()
