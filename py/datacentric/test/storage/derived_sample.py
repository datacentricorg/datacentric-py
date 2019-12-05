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
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.storage.data import Data
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.base_sample import BaseSample, BaseSampleKey
from datacentric.test.storage.element_sample import ElementSample


@attr.s(slots=True, auto_attribs=True)
class DerivedSample(BaseSample):
    """Derived class sample."""

    double_element2: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    string_element2: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    list_of_string: List[str] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    list_of_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    list_of_nullable_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    data_element: ElementSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    data_element_list: List[ElementSample] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    key_element: Union[str, BaseSampleKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    key_element_list: List[Union[str, BaseSampleKey]] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""
