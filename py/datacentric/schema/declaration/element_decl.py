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
from datacentric.schema.declaration.param_decl import ParamDecl
from datacentric.schema.declaration.yes_no import YesNo


@attr.s(slots=True, auto_attribs=True)
class ElementDecl(ParamDecl):
    """Definition of a single element within type declaration."""

    hidden: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Flag indicating a hidden element.

    Hidden elements are present in the API but hidden in the user interface,
    except in developer mode.
    """

    additive: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Optional flag indicating if the element is additive. For additive elements,
    total column can be shown in the user interface.

    This field has no effect on the API and affects only the user interface.
    """

    category: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Provides the ability to group the elements in the user interface.

    This field has no effect on the API and affects only the user interface.
    """

    format: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Formatting string for the element applied in the user interface.

    TODO - specify formatting convention and accepted format strings.
    """

    output: YesNo = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Flag indicating an output element.

    Output elements will be readonly in the user interface. They can only be populated through the API.

    TODO - this duplicates ModificationType, need to consolidate.
    """

    alternate_of: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Specify the name of the element for which the current element as an alternate.

    In the user interface, only one of the alternate elements can be provided.
    The default element to be provided is the one for which alternates are specified,
    while the alternates have to be selected explicitly.
    """
