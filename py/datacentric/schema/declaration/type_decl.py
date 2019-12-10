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
from datacentric.schema.declaration.type_decl_key import TypeDeclKey
from datacentric.schema.declaration.handler_declare_block import HandlerDeclareBlock
from datacentric.schema.declaration.handler_implement_block import HandlerImplementBlock
from datacentric.schema.declaration.element_decl import ElementDecl
from datacentric.schema.declaration.index_elements import IndexElements
from datacentric.schema.declaration.module_key import ModuleKey
from datacentric.schema.declaration.type_kind import TypeKind
from datacentric.schema.declaration.yes_no import YesNo


@attr.s(slots=True, auto_attribs=True)
class TypeDecl(Record):
    """Language neutral description of a data class."""

    module: Union[str, ModuleKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Module reference."""

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Type name is unique when combined with module."""

    label: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    If specified, will be used in the user interface instead of the name.

    This field has no effect on the API and affects only the user interface.
    """

    comment: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Detailed description of the type."""

    category: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Dot delimited category providing the ability to group the types inside
    the module. Typically maps to the folder where source code for the
    data type resides.

    This field has no effect on the API and affects only the user interface.
    """

    kind: TypeKind = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Type kind."""

    is_record: bool = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Indicates if type is derived from Record.

    TODO - overlaps with Kind, consolidate?
    """

    inherit: Union[str, TypeDeclKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Reference to the parent type.

    The record can only have a single parent type,
    however it can include multiple data interfaces.
    """

    declare: HandlerDeclareBlock = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Handler declaration block."""

    implement: HandlerImplementBlock = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Handler implementation block."""

    elements: List[ElementDecl] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """
    Each item within this list specifies one element (field)
    of the current type.
    """

    keys: List[str] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """Array of key element names."""

    index: List[IndexElements] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """
    Array of database index definitions, each item representing a single index.

    TODO - make plural when switching from XML to JSON
    """

    immutable: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Immutable flag.

    TODO - introduce an attribute to specify this flag in source code.
    """

    permanent: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Flag indicating a record that is always saved permanently.

    TODO - introduce an attribute to specify this flag in source code.
    """

    def to_key(self) -> str:
        """Get TypeDecl key."""
        return 'TypeDecl=' + ';'.join([self.module.split('=', 1)[1], self.name])

    @classmethod
    def create_key(cls, *, module: Union[str, ModuleKey], name: str) -> Union[str, TypeDeclKey]:
        """Create TypeDecl key."""
        return 'TypeDecl=' + ';'.join([module.split('=', 1)[1], name])
