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
from typing import Union
from datacentric.storage.data import Data
from datacentric.schema.declaration.enum_decl_key import EnumDeclKey
from datacentric.schema.declaration.type_decl_key import TypeDeclKey
from datacentric.schema.declaration.yes_no import YesNo


@attr.s(slots=True, auto_attribs=True)
class ParamDecl(Data):
    """
    Definition of a handler parameter that is also used as
    base class of element declaration.
    """

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Element name."""

    label: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    If specified, will be used in the user interface instead of the name.

    This field has no effect on the API and affects only the user interface.
    """

    comment: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Detailed description of the element."""

    enum: Union[str, EnumDeclKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Reference the declaration of enum contained
    by the current element.
    """

    data: Union[str, TypeDeclKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Reference to declaration of the data type
    contained by the current element.

    The referenced type must have TypeKind=Element.
    """

    key: Union[str, TypeDeclKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Reference to declaration of the data type for
    which the key is contained by the current element.

    The referenced type must not have TypeKind=Element.
    """

    vector: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Specifies that the current element is a list."""

    optional: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Indicates that the element is optional.

    By default, all elements are required. Use this flag
    to specify that an element is optional.
    """
