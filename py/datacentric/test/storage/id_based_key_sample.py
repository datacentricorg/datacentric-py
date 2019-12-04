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
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.test.storage.base_sample import BaseSampleKey
from datacentric.testing.unit_test import UnitTestKey, UnitTest


@attr.s(slots=True, auto_attribs=True)
class IdBasedKeySample(TypedRecord[IdBasedKeySampleKey]):
    string_element: str = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class IdBasedKeySampleKey(TypedKey['IdBasedKeySample']):
    id_: ObjectId = attr.ib(default=None, kw_only=True)
