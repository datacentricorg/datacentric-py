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
from datacentric.storage.record import Record


@attr.s(slots=True, auto_attribs=True)
class DatesSample(Record):
    """Base class of sample data for data source testing."""

    record_name: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

    local_date_element: int = attr.ib(default=None, kw_only=True, metadata={'type': 'LocalDate'})
    """Sample element."""

    local_time_element: int = attr.ib(default=None, kw_only=True, metadata={'type': 'LocalTime'})
    """Sample element."""

    local_minute_element: int = attr.ib(default=None, kw_only=True, metadata={'type': 'LocalMinute'})
    """Sample element."""

    local_date_time_element: int = attr.ib(default=None, kw_only=True, metadata={'type': 'LocalDateTime'})
    """Sample element."""

    instant_element: dt.datetime = attr.ib(default=None, kw_only=True, metadata={'type': 'Instant'})
    """Sample element."""

    date_element: dt.date = attr.ib(default=None, kw_only=True)
    """LocalDate alternative element."""

    time_element: dt.time = attr.ib(default=None, kw_only=True)
    """LocalTime alternative element."""

    date_time_element: dt.datetime = attr.ib(default=None, kw_only=True)
    """LocalDateTime alternative element."""

    def to_key(self) -> str:
        """Get BaseSample key."""
        return 'DatesSample=' + self.record_name

    @classmethod
    def create_key(cls, *, record_name: str) -> str:
        """Create BaseSample key."""
        return 'DatesSample=' + record_name
