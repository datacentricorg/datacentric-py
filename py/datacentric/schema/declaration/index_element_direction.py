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

from enum import IntEnum


class IndexElementDirection(IntEnum):
    """
    Specifies the direction of element within database index
    defined for the type.
    """

    Empty = 0,
    """
    Indicates that enum value is not set.

    In programming languages where enum defaults to the first item when
    not set, making Empty the first item prevents unintended assignment
    of a meaningful value.
    """

    Ascending = 1,
    """Ascending direction of the element inside the index."""

    Descending = 2,
    """Descending of the element inside the index."""
