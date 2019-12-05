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
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.storage.data_source import DataSource
from datacentric.test.storage.root_sample_key import RootSampleKey


@attr.s(slots=True, auto_attribs=True)
class RootSample(Record):
    """
    Root record is always stored in root dataset,
    even if another dataset is specified in save
    method.
    """

    record_name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    # --- METHODS

    def to_key(self) -> Union[str, RootSampleKey]:
        """Create key string from the current record."""
        return 'RootSample=' + self.record_name

    # --- STATIC

    @classmethod
    def create_key(cls, *, record_name: str) -> Union[str, RootSampleKey]:
        """Create key string from key elements."""
        return 'RootSample=' + record_name

    @classmethod
    def load(cls, data_source: DataSource, key: Union[str, RootSampleKey],
             data_set: ObjectId) -> 'RootSample':
        """Load record by key (error message if not found)."""
        return data_source.load_by_key(RootSample, key, data_set)

    @classmethod
    def load_or_null(cls, data_source: DataSource, key: Union[str, RootSampleKey],
                     data_set: ObjectId) -> Optional['RootSample']:
        """Load record by key (return null if not found)."""
        return data_source.load_or_null_by_key(RootSample, key, data_set)
