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


@attr.s(slots=True)
class DeletedRecord(Record):
    """
    When returned by the data source, this record has the same
    effect as if no record was found. It is used to indicate
    a deleted record when audit log must be preserved.
    """

    _key: str = attr.ib(default=None, kw_only=True)
    """Attribute to hold key."""

    @property
    def key(self) -> str:
        """
        String key consists of semicolon delimited primary key elements:

        KeyElement1;KeyElement2

        To avoid serialization format uncertainty, key elements
        can have any atomic type except Double.
        """

        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    def to_key(self) -> str:
        """Deleted record key."""
        return self._key
