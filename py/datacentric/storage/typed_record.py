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
import attr
from abc import ABC
from bson import ObjectId, Int64
from typing import TypeVar, List, ClassVar, Tuple

from datacentric.storage.class_info import ClassInfo
from datacentric.storage.record import Record

TKey = TypeVar('TKey')


@attr.s(slots=True)
class TypedRecord(Record, ABC):
    """Base class of records stored in data source."""
    _keys: ClassVar[Tuple[str]] = ()

    @property
    def key(self) -> str:
        """String key consists of semicolon delimited primary key elements. To avoid serialization format uncertainty,
        key elements can have any atomic type except float.
        """
        data_slots = attr.fields(type(self))
        key_slots = [x.name for x in data_slots if x.name in self._keys]

        tokens: List[str] = []
        for slot in key_slots:
            attr_value = self.__getattribute__(slot)
            attr_type = type(attr_value)
            if attr_value is None:
                raise Exception(f'Key element {slot} of type {type(self).__name__} is null. '
                                f'Null elements are not permitted in key.')
            elif attr_type == str:
                if attr_value == '':
                    raise Exception(f'String key element {slot} is empty. Empty elements are not permitted in key.')
                if ';' in attr_value:
                    raise Exception(f'Key element {slot} of type {type(self).__name__} includes semicolon delimiter. '
                                    f'The use of this delimiter is reserved for separating key tokens.')
                token = attr_value
            elif attr_type == float:
                raise Exception(f'Key element {slot} of type {type(self).__name__} has type float. '
                                f'Elements of this type cannot be part of key due to serialization format uncertainty.')

            elif attr_type == bool:
                token = 'true' if attr_value else 'false'
            elif attr_type == int:
                token = str(attr_value)
            elif attr_type == Int64:
                token = str(attr_value)
            elif attr_type == ObjectId:
                token = str(attr_value)
            elif issubclass(attr_type, IntEnum):
                token = attr_value.name
            else:
                raise Exception(f'Key element {slot} of type {type(self).__name__} has type {attr_type.__name__} '
                                f'that is not one of the supported key element types. Available key element types are '
                                f'string, double, bool, int, long, LocalDate, LocalTime, LocalMinute, LocalDateTime, '
                                f'LocalMinute, ObjectId, or Enum.')
            tokens.append(token)

        return ';'.join(tokens)

    @key.setter
    def key(self, value: str):
        pass

    def to_key(self) -> TKey:
        """This conversion method creates a new key, populates key elements of the
        created key by the values taken from the record.
        """

        key_type = ClassInfo.get_key_from_record(type(self))
        key = key_type()
        key.populate_from(self)
        return key
