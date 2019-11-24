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
from datacentric.log.log_verbosity import LogVerbosity
from datacentric.log.file_log import FileLog
from datacentric.storage.context import Context


class TestFileLog(unittest.TestCase, UnitTest):
    def test_smoke(self):
        """Smoke test"""

        # File name for log output
        file_path: str = __file__.replace(".py", "test_smoke.approved.txt")

        # Initialize FileLog object with Verify verbosity
        # to ensure all messages are displayed, because default
        # verbosity is Error
        file_log: FileLog = FileLog()
        file_log.verbosity = LogVerbosity.Verify
        file_log.log_file_path = file_path
        file_log.init(Context()) # TODO - provide actual context

        # Test logging
        file_log.error('Title for error', 'Description for error')
        file_log.warning('Title for warning', 'Description for warning')
        file_log.info('Title for info', 'Description for info')
        file_log.assert_(True, 'Title for true assert', 'Description for true assert')
        file_log.assert_(False, 'Title for false assert', 'Description for false assert')
        file_log.info('Multi-line title\nSecond line of title',
                      'Multi-line description\nSecond line of description')

if __name__ == "__main__":
    unittest.main()
