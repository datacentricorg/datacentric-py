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
from typing import TypeVar, Generic, List
from datacentric.storage.class_info import ClassInfo
from datacentric.storage.key import Key
from datacentric.storage.record import Record

TKey = TypeVar('TKey')


@attr.s(slots=True)
class TypedRecord(Generic[TKey], Record, ABC):
    """Base class of records stored in data source."""

    @property
    def key(self) -> str:
        """String key consists of semicolon delimited primary key elements. To avoid serialization format uncertainty,
        key elements can have any atomic type except float.
        """
        key_type = ClassInfo.get_key_from_record(type(self))

        key_slots = key_type.__slots__
        if type(key_slots) is str:
            key_slots = [key_slots]
        data_slots = self.__slots__
        if type(data_slots) is str:
            data_slots = [data_slots]

        if len(key_slots) > len(data_slots):
            raise Exception(
                f'Key type {key_type.__name__} has more elements than {self.__name__}.')

        tokens: List[str] = []
        for slot in key_slots:
            token = Key.get_key_token(self, slot)
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
