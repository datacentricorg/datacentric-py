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

import re
from typing import Pattern


class StringUtil():
    """
    Static helper class for str.
    """

    __first_cap_re: Pattern = re.compile('(.)([A-Z][a-z]+)')
    __all_cap_re: Pattern = re.compile('([a-z0-9])([A-Z])')

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """
        Converts strings to PascalCase also removing underscores.
        """
        result: str = ''.join(x for x in name.title() if not x == '_')
        return result

    @staticmethod
    def to_snake_case(name: str) -> str:
        """
        Converts PascalCase strings to snake_case.
        """
        s1: str = StringUtil.__first_cap_re.sub(r'\1_\2', name)
        result: str = StringUtil.__all_cap_re.sub(r'\1_\2', s1).lower()
        return result
