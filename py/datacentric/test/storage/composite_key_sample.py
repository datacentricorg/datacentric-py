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
from datacentric.storage.record import Record


@attr.s(slots=True, auto_attribs=True)
class CompositeKeySample(Record):
    """Data type sample with composite key."""

    key_element1: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """String key element."""

    key_element2: str = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'key': 'BaseSample'})
    """Another key."""

    key_element3: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """String key element."""

    element4: str = attr.ib(default=None, kw_only=True, metadata={'optional': True, 'key': 'CompositeKeySample'})
    """Key to the same type."""

    def to_key(self) -> str:
        """Get CompositeKeySample key."""
        return 'CompositeKeySample=' + ';'.join([self.key_element1,
                                                 self.key_element2.split('=', 1)[1],
                                                 self.key_element3])

    @classmethod
    def create_key(cls, *, key_element1: str, key_element2: str, key_element3: str) -> str:
        """Create CompositeKeySample key."""
        return 'CompositeKeySample=' + ';'.join([key_element1,
                                                 key_element2.split('=', 1)[1],
                                                 key_element3])
