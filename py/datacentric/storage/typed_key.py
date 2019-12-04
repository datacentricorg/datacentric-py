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
from typing import TypeVar, Generic
from datacentric.storage.class_info import ClassInfo
from datacentric.storage.key import Key

TRecord = TypeVar('TRecord')


@attr.s(slots=True)
class TypedKey(Generic[TRecord], Key, ABC):
    """Base class of a foreign key.
    Generic parameter TRecord make it possible to bound key type to its record.
    Any elements of defined in the class derived from this one
    become key tokens.
    """

    def populate_from(self, record: TRecord) -> None:
        """Populate key attributes by taking them from the matching
        attributes of the argument record.
        """
        key_elements = attr.fields(type(self))
        record_elements = attr.fields(type(record))

        if len(record_elements) < len(key_elements):
            raise Exception(
                f'Root data type {type(record).__name__} has fewer elements than key type {type(self).__name__}.')

        for key_element in key_elements:
            value = record.__getattribute__(key_element.name)
            self.__setattr__(key_element.name, value)
