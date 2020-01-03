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

from datacentric.attributes.handler_attribute import handler
from datacentric.storage.record import Record
from datacentric.test.storage.sample_enum import SampleEnum


@attr.s(slots=True, auto_attribs=True)
class BaseSample(Record):
    """Base class of sample data for data source testing."""

    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_date_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'LocalDate'})
    """Sample element."""

    enum_value: SampleEnum = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    local_time_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'LocalTime'})
    """Sample element."""

    local_minute_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'LocalMinute'})
    """Sample element."""

    local_date_time_element: int = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'LocalDateTime'})
    """Sample element."""

    instant_element: dt.datetime = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'type': 'Instant'})
    """Sample element."""

    def to_key(self) -> str:
        """Get BaseSample key."""
        return 'BaseSample=' + ';'.join([self.record_name, str(self.record_index)])

    @classmethod
    def create_key(cls, *, record_name: str, record_index: int) -> str:
        """Create BaseSample key."""
        return 'BaseSample=' + ';'.join([record_name, str(record_index)])

    @handler
    def non_virtual_base_handler(self):
        """Non-virtual handler defined in base type."""
        pass

    @handler
    def virtual_base_handler(self):
        """Virtual handler defined in base type."""
        pass
