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
from bson import ObjectId
from datacentric.storage.record import Record


@attr.s(slots=True, auto_attribs=True)
class IdBasedKeySample(Record):
    """A sample type where the only key element is the record's Id."""

    string_element: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    def to_key(self) -> str:
        """Get IdBasedKeySample key."""
        return 'IdBasedKeySample=' + str(self.id_)

    @classmethod
    def create_key(cls, *, id_: ObjectId) -> str:
        """Create IdBasedKeySample key."""
        return 'IdBasedKeySample=' + str(id_)
