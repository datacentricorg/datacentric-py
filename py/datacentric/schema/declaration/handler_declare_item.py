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
from typing import List
from datacentric.storage.data import Data
from datacentric.schema.declaration.param_decl import ParamDecl
from datacentric.schema.declaration.handler_type import HandlerType
from datacentric.schema.declaration.yes_no import YesNo


@attr.s(slots=True, auto_attribs=True)
class HandlerDeclareItem(Data):
    """
    Represents a single item within handler declaration block.

    Every declared handler must be implemented in this
    class or its non-abstract descendant, error message
    otherwise.
    """

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Handler name."""

    label: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Handler label."""

    comment: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Handler comment."""

    type: HandlerType = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Handler type.

    TODO - rename both type and element name to HandlerKind
    """

    params: List[ParamDecl] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """Handler parameters."""

    static: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """If this flag is set, handler will be static, otherwise it will be non-static."""

    hidden: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    If this flag is set, handler will be hidden in the user interface
    except in developer mode.
    """

    category: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Category."""
