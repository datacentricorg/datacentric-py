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
from datacentric.schema.declaration.index_element import IndexElement


@attr.s(slots=True, auto_attribs=True)
class IndexElements(Data):
    """
    Specifies database index for the type by listing elements
    including in the index and their direction.

    A type may have multiple indexes.
    """

    name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Name of the index."""

    element: List[IndexElement] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """
    Elements within the index.

    TODO - make plural when moving from XML to JSON declaration
    """
