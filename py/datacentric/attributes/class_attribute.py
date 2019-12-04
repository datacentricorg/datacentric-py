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

from abc import ABC


class ClassAttribute(ABC):
    """
    Abstract base class for custom class attributes.

    Class attributes are assigned to the class via static element
    class_attributes which by default is empty. The user can then
    iterate over or search in this list to find the desired attribute.

    Declaration of the static element attributes in Data:

    class_attributes: List[ClassAttribute]
    """
