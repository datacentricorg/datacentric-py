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
from typing import List, ClassVar, Tuple, Union, Optional
from abc import ABC
from bson import ObjectId
from datacentric.date_time.local_date import LocalDate, LocalDateHint
from datacentric.date_time.local_time import LocalTime, LocalTimeHint
from datacentric.date_time.local_minute import LocalMinute, LocalMinuteHint
from datacentric.date_time.local_date_time import LocalDateTime, LocalDateTimeHint
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.storage.data_source import DataSource
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.test.storage.base_sample_key import BaseSampleKey


@attr.s(slots=True, auto_attribs=True)
class BaseSample(Record):
    """Base class sample."""

    record_id: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_element: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_time_element: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_minute_element: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_time_element: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    enum_value: EnumSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    # --- METHODS

    def to_key(self) -> Union[str, BaseSampleKey]:
        """Create key string from the current record."""
        return 'BaseSample=' + self.record_id + ';' + str(self.record_index)

    # --- STATIC

    @classmethod
    def load(cls, data_source: DataSource, key: Union[str, BaseSampleKey],
             data_set: ObjectId) -> 'BaseSample':
        """Load record by key (error message if not found)."""
        return data_source.load_by_key(BaseSample, key, data_set)

    @classmethod
    def load_or_null(cls, data_source: DataSource, key: Union[str, BaseSampleKey],
                     data_set: ObjectId) -> Optional['BaseSample']:
        """Load record by key (return null if not found)."""
        return data_source.load_or_null_by_key(BaseSample, key, data_set)

    @classmethod
    def create_key(cls, *, record_id: str, record_index: int) -> Union[str, BaseSampleKey]:
        """Create key string from key elements."""
        return 'BaseSample=' + record_id + ';' + str(record_index)
