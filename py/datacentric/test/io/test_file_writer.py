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
import sys
from datacentric.testing.unit_test import UnitTest
from datacentric.io.text_writer import TextWriter
from datacentric.io.file_writer import FileWriter

class TestFileWriter(unittest.TestCase, UnitTest):
    def test_smoke(self):
        """Smoke test"""
        file_path: str = __file__.replace(".py","_output.txt")
        file_writer: TextWriter = FileWriter(file_path)
        file_writer.write('A')
        file_writer.write_line('BC')
        file_writer.write_eol()
        file_writer.write_line('DEF')
        file_writer.flush()

if __name__ == "__main__":
    unittest.main()
