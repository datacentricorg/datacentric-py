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
from typing import Union, Optional, List, Any
import datetime as dt
from bson import ObjectId
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.test.storage.base_sample_key import BaseSampleKey
from datacentric.test.storage.composite_key_sample_key import CompositeKeySampleKey


@attr.s(slots=True, auto_attribs=True)
class CompositeKeySample(Record):
    """Sample for a class with composite key."""

    key_element1: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

    key_element2: Union[str, BaseSampleKey] = attr.ib(default=None, kw_only=True)
    """Sample element."""

    key_element3: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

    # --- METHODS

    def to_key(self) -> Union[str, CompositeKeySampleKey]:
        """Create key string from the current record."""
        return 'CompositeKeySample=' + ';'.join(
            [
                self.key_element1,
                self.key_element2.replace('BaseSample=', ''),
                self.key_element3
            ]
        )

    # --- STATIC

    @classmethod
    def create_key(cls, *, key_element1: str, key_element2: Union[str, BaseSampleKey], key_element3: str) -> Union[str, BaseSampleKey]:
        """Create key string from key elements."""
        return 'CompositeKeySample=' + ';'.join(
            [
                key_element1,
                key_element2.replace('BaseSample=', ''),
                key_element3
            ]
        )
