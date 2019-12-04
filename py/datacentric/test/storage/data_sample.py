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

from datacentric.date_time.local_date import LocalDate, LocalDateHint
from datacentric.date_time.local_time import LocalTime, LocalTimeHint
from datacentric.date_time.local_minute import LocalMinute, LocalMinuteHint
from datacentric.date_time.local_date_time import LocalDateTime, LocalDateTimeHint
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.data import Data


@attr.s(slots=True, auto_attribs=True)
class ElementSample(Data):
    double_element3: float = attr.ib(default=None, kw_only=True)
    string_element3: str = attr.ib(default=None, kw_only=True)


class SampleEnum(IntEnum):
    Empty = 0
    EnumValue1 = 1
    EnumValue2 = 2


@attr.s(slots=True, auto_attribs=True)
class BaseSample(TypedRecord):
    _keys: ClassVar[Tuple[str]] = ('record_id', 'record_index')
    record_id: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_element: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_time_element: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_minute_element: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_time_element: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    enum_value: SampleEnum = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})


@attr.s(slots=True, auto_attribs=True)
class BaseSampleKey(TypedKey[BaseSample]):
    pass


@attr.s(slots=True, auto_attribs=True)
class DerivedSample(BaseSample):
    double_element2: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    string_element2: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_string: List[str] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_nullable_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    data_element: ElementSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    data_element_list: List[ElementSample] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    key_element: Union[str, BaseSampleKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    key_element_list: List[Union[str, BaseSampleKey]] = attr.ib(default=None, kw_only=True, metadata={'optional': True})


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSample(TypedRecord):
    _keys: ClassVar[Tuple[str]] = ('string_token', 'bool_token', 'int_token', 'local_date_token', 'local_time_token',
                                   'local_minute_token', 'local_date_time_token', 'enum_token')
    string_token: str = attr.ib(default=None, kw_only=True)
    bool_token: bool = attr.ib(default=None, kw_only=True)
    int_token: int = attr.ib(default=None, kw_only=True)
    local_date_token: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True)
    local_time_token: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True)
    local_minute_token: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True)
    local_date_time_token: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True)
    enum_token: SampleEnum = attr.ib(default=None, kw_only=True)
    record_index: int = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSampleKey(TypedKey[NullableElementsSample]):
    pass
