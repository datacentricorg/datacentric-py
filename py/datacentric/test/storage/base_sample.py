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
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.data_source import DataSource
from datacentric.test.storage.enum_sample import EnumSample


@attr.s(slots=True, auto_attribs=True)
class BaseSample(TypedRecord):
    record_id: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_element: Union[int, LocalDateHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_time_element: Union[int, LocalTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_minute_element: Union[int, LocalMinuteHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_time_element: Union[int, LocalDateTimeHint] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    enum_value: EnumSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})

    # --- STATIC

    @classmethod
    def load(cls, data_source: DataSource, key: Union[str, BaseSampleKey],
             data_set: ObjectId) -> BaseSample:
        """Load record by key (error message if not found)."""
        return data_source.load_by_key(key, data_set)

    @classmethod
    def load_or_null(cls, data_source: DataSource, key: Union[str, BaseSampleKey],
                     data_set: ObjectId) -> Optional[BaseSample]:
        """Load record by key (return null if not found)."""
        return data_source.load_or_null_by_key(key, data_set)


@attr.s(slots=True, auto_attribs=True)
class BaseSampleKey(ABC):

    @classmethod
    def from_attribs(cls, *, record_id: str, record_index: int) -> Union[str, BaseSampleKey]:
        """Create key string from key element params."""
        return f'BaseSample={record_id};{record_index}'

    @classmethod
    def from_record(cls, rec: BaseSample) -> Union[str, BaseSampleKey]:
        """Create key string from key elements in the record."""
        return f'BaseSample={rec.record_id};{rec.record_index}'