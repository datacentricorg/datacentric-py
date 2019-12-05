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
import unittest
import datetime as dt
from bson import ObjectId
from datacentric.storage.record import Record
from datacentric.storage.key import Key
from datacentric.test.storage.base_sample import BaseSample, BaseSampleKey


@attr.s(slots=True, auto_attribs=True)
class CompositeKeySample(Record):
    """Sample for a class with composite key."""

    key_element1: str = attr.ib(default=None, kw_only=True)
    """Sample element."""

    key_element2: BaseSampleKey = attr.ib(default=None, kw_only=True)
    """Sample element."""

    key_element3: str = attr.ib(default=None, kw_only=True)
    """Sample element."""



@attr.s(slots=True, auto_attribs=True)
class CompositeKeySampleKey(TypedKey['CompositeKeySample']):
    key_element1: str = attr.ib(default=None, kw_only=True)
    key_element2: BaseSampleKey = attr.ib(default=None, kw_only=True)
    key_element3: str = attr.ib(default=None, kw_only=True)
