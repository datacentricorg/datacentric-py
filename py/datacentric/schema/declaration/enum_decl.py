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
from typing import List, Union
from datacentric.storage.record import Record
from datacentric.schema.declaration.enum_decl_key import EnumDeclKey
from datacentric.schema.declaration.enum_item import EnumItem
from datacentric.schema.declaration.module_key import ModuleKey


@attr.s(slots=True, auto_attribs=True)
class EnumDecl(Record):
    """Language neutral description of an enumeration."""

    module: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Module reference."""

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Enum name is unique when combined with module."""

    label: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Optional label is used in the user interface, but not in serialization.

    If not specified, item name is used instead.
    """

    comment: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Detailed description of the enum."""

    category: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Category."""

    items: List[EnumItem] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """Array of enum items."""

    def to_key(self) -> str:
        """Get EnumDecl key."""
        return 'EnumDecl=' + ';'.join([self.module.split('=', 1)[1], self.name])

    @classmethod
    def create_key(cls, *, module: str, name: str) -> str:
        """Create EnumDecl key."""
        return 'EnumDecl=' + ';'.join([module.split('=', 1)[1], name])
