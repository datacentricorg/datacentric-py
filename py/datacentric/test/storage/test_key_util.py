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
from datacentric.storage.unit_test_context import UnitTestContext
from datacentric.storage.key_util import KeyUtil


class TestKeyUtil(unittest.TestCase):
    """Unit tests for KeyUtil."""

    def test_smoke(self):
        """Smoke test for KeyUtil."""

        with UnitTestContext() as context:

            # Remove prefix, correct type is specified
            self.assertTrue(KeyUtil.remove_prefix('MyType=A;B;C', 'MyType') == 'A;B;C')

            # Remove prefix, wrong type is specified, throws
            with self.assertRaises(Exception):
                KeyUtil.remove_prefix('MyType=A;B;C', 'OtherType')

            # Get token, correct type and valid index are specified
            self.assertTrue(KeyUtil.get_token('MyType=A;B;C', 'MyType', 3, 1) == 'B')

            # Get token, wrong type is specified
            with self.assertRaises(Exception):
                KeyUtil.get_token('MyType=A;B;C', 'OtherType', 3, 1)

            # Get token, wrong number of tokens specified
            with self.assertRaises(Exception):
                KeyUtil.get_token('MyType=A;B', 'MyType', 3, 1)

            # Get token, index out of range
            with self.assertRaises(Exception):
                KeyUtil.get_token('MyType=A;B;C', 'MyType', 3, 3)


if __name__ == "__main__":
    unittest.main()
