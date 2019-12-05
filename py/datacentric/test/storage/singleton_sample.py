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
from typing import Union
from datacentric.storage.record import Record
from datacentric.test.storage.singleton_sample_key import SingletonSampleKey


@attr.s(slots=True, auto_attribs=True)
class SingletonSample(Record):
    """
    A sample data type with no key elements.

    Only one record of this type can be present in a given dataset.
    """

    string_element: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Sample element."""

    def to_key(self) -> Union[str, SingletonSampleKey]:
        """Create key string from the current record."""
        return 'SingletonSample='

    @classmethod
    def create_key(cls) -> Union[str, SingletonSampleKey]:
        """Create key string from key elements."""
        return 'SingletonSample='
