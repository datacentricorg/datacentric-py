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
from datacentric.test.storage.enum_sample import EnumSample


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSample(TypedRecord):
    string_token: str = attr.ib(default=None, kw_only=True)
    bool_token: bool = attr.ib(default=None, kw_only=True)
    int_token: int = attr.ib(default=None, kw_only=True)
    local_date_token: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True)
    local_time_token: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True)
    local_minute_token: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True)
    local_date_time_token: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True)
    enum_token: EnumSample = attr.ib(default=None, kw_only=True)
    record_index: int = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSampleKey(TypedKey[NullableElementsSample]):
    pass
