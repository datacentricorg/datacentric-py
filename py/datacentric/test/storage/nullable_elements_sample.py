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
from typing import Union, Optional, List, Any
from enum import IntEnum
from typing import List, ClassVar, Tuple, Union
from datacentric.date_time.local_date import LocalDate, LocalDateHint
from datacentric.date_time.local_time import LocalTime, LocalTimeHint
from datacentric.date_time.local_minute import LocalMinute, LocalMinuteHint
from datacentric.date_time.local_date_time import LocalDateTime, LocalDateTimeHint
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.storage.data import Data
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.nullable_elements_sample_key import NullableElementsSampleKey


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSample(Record):
    """Sample class with every type of nullable element."""

    string_token: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

    bool_token: bool = attr.ib(default=None, kw_only=True)
    """Sample element."""

    int_token: int = attr.ib(default=None, kw_only=True)
    """Sample element."""

    local_date_token: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True)
    """Sample element."""

    local_time_token: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True)
    """Sample element."""

    local_minute_token: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True)
    """Sample element."""

    local_date_time_token: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True)
    """Sample element."""

    enum_token: EnumSample = attr.ib(default=None, kw_only=True)
    """Sample element."""

    record_index: int = attr.ib(default=None, kw_only=True)
    """Sample element."""

    # --- METHODS

    def to_key(self) -> Union[str, NullableElementsSampleKey]:
        """Create key string from the current record."""
        return 'NullableElementsSample=' + self.string_token
