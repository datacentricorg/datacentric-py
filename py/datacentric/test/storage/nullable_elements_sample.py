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
import datetime as dt
from typing import Union
from datacentric.storage.record import Record
from datacentric.test.storage.nullable_elements_sample_key import NullableElementsSampleKey
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.instant import Instant


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSample(Record):
    """Key class that has all of the permitted nullable key elements included."""

    string_token: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    bool_token: bool = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    int_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    long_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'long'})
    """Sample element."""

    local_date_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_time_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_minute_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_time_token: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    instant_token: dt.datetime = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    enum_token: EnumSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    def to_key(self) -> str:
        """Get NullableElementsSample key."""
        return 'NullableElementsSample=' + ';'.join([self.string_token,
                                                     str(self.bool_token).lower(),
                                                     str(self.int_token),
                                                     str(self.long_token),
                                                     str(self.local_date_token),
                                                     str(self.local_time_token),
                                                     str(self.local_minute_token),
                                                     str(self.local_date_time_token),
                                                     Instant.to_str(self.instant_token),
                                                     self.enum_token.name])

    @classmethod
    def create_key(cls, *, string_token: str,
                   bool_token: bool,
                   int_token: int,
                   long_token: int,
                   local_date_token: int,
                   local_time_token: int,
                   local_minute_token: int,
                   local_date_time_token: int,
                   instant_token: dt.datetime,
                   enum_token: EnumSample) -> str:
        """Create NullableElementsSample key."""
        return 'NullableElementsSample=' + ';'.join([string_token,
                                                     str(bool_token).lower(),
                                                     str(int_token),
                                                     str(long_token),
                                                     str(local_date_token),
                                                     str(local_time_token),
                                                     str(local_minute_token),
                                                     str(local_date_time_token),
                                                     Instant.to_str(instant_token),
                                                     enum_token.name])
