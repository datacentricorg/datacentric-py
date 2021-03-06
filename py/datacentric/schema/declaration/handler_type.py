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


class HandlerType(IntEnum):
    """
    Handler type enumeration.

    TODO - rename both type and element name to HandlerKind
    """

    Empty = 0,
    """
    Indicates that enum value is not set.

    In programming languages where enum defaults to the first item when
    not set, making Empty the first item prevents unintended assignment
    of a meaningful value.
    """

    Job = 1,
    """
    Job handler is an action that can be invoked via the UI.

    Return type is not allowed. Input parameters are allowed.
    """

    Process = 2,
    """
    Process handler represents a process that can be launched
    from the UI. Once launched, the process continues until it
    terminates itself, or is terminated from the user interface.

    Return type is not allowed. Input params are allowed.
    """

    Viewer = 3,
    """
    Viewer handler.

    Return type is allowed. Input params are not allowed.
    """

    Editor = 4,
    """
    Viewer Editor. Return type is allowed. Input params are not allowed.

    TODO - consider deprecating
    """
