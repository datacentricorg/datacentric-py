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

import attr
from enum import IntEnum
from typing import List, ClassVar, Tuple, Union
from datacentric.storage.data import Data


@attr.s(slots=True, auto_attribs=True)
class ElementSample(Data):
    """Element type sample."""
    double_element3: float = attr.ib(default=None, kw_only=True)
    """Sample element."""

    string_element3: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

