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
from datacentric.testing.unit_test import UnitTest
from datacentric.types.string_util import StringUtil
from datacentric.io.text_writer import TextWriter
from datacentric.io.file_writer import FileWriter

class TestStringUtil(unittest.TestCase, UnitTest):
    def test_smoke(self):
        """Smoke test"""
        file_path: str = __file__.replace(".py",".approved.txt")
        file_writer: TextWriter = FileWriter(file_path)

        # Does not remove space TODO - check that Humanizer does in C#
        file_writer.write_line(StringUtil.to_pascal_case('abc def'))
        file_writer.write_line(StringUtil.to_pascal_case('abc_def'))

        # Does not remove space TODO - check that Humanizer does in C#
        file_writer.write_line(StringUtil.to_snake_case('Abc Def'))
        file_writer.write_line(StringUtil.to_snake_case('AbcDef'))

if __name__ == "__main__":
    unittest.main()
