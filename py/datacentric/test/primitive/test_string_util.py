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
from datacentric.storage.context import Context
from datacentric.primitive.string_util import StringUtil


class TestStringUtil(unittest.TestCase):
    """Unit tests for StringUtil."""

    def test_smoke(self):
        """Smoke test"""
        context: Context = self.create_method_context()

        # Does not remove space TODO - check that Humanizer does in C#
        context.log.verify(StringUtil.to_pascal_case('abc def'))
        context.log.verify(StringUtil.to_pascal_case('abc_def'))

        # Does not remove space TODO - check that Humanizer does in C#
        context.log.verify(StringUtil.to_snake_case('Abc Def'))
        context.log.verify(StringUtil.to_snake_case('AbcDef'))


if __name__ == "__main__":
    unittest.main()
