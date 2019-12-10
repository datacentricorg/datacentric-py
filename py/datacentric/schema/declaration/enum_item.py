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
from datacentric.storage.data import Data


@attr.s(slots=True, auto_attribs=True)
class EnumItem(Data):
    """Item in an enumeration"""

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Name of the item will be used in the generated code."""

    label: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Optional label is used in the user interface, but not in serialization.

    If not specified, item name is used instead.
    """

    comment: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Detailed description of the item."""
