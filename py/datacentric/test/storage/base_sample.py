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
from datacentric.test.storage.base_sample_key import BaseSampleKey
from datacentric.test.storage.enum_sample import EnumSample
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.instant import Instant


@attr.s(slots=True, auto_attribs=True)
class BaseSample(Record):
    """Base class of sample data for data source testing."""

    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    enum_value: EnumSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_time_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_minute_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_time_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    instant_element: dt.datetime = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    def to_key(self) -> str:
        """Get BaseSample key."""
        return 'BaseSample=' + ';'.join([self.record_name, str(self.record_index)])

    @classmethod
    def create_key(cls, *, record_name: str, record_index: int) -> Union[str, BaseSampleKey]:
        """Create BaseSample key."""
        return 'BaseSample=' + ';'.join([record_name, str(record_index)])

    def non_virtual_base_handler(self):
        """Non-virtual handler defined in base type."""
        pass

    def virtual_base_handler(self):
        """Virtual handler defined in base type."""
        pass
