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
from abc import ABC
from typing import Tuple
from datacentric.attributes.class_attribute import ClassAttribute


@attr.s(slots=True)
class Data(ABC):
    """ Abstract base class for data structures"""

    class_attributes: Tuple[ClassAttribute, ...] = None
    """
    Class attributes are assigned to the class via static element
    class_attributes which by default is empty. The user can then
    iterate over or search in this list to find the desired attribute.
    """
