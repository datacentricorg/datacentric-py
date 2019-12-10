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
from datacentric.schema.declaration.module_key import ModuleKey


@attr.s(slots=True, auto_attribs=True)
class Module(Record):
    """
    Module is a way to organize a group of data types within a package.

    Module name is a dot delimited string which in most cases corresponds
    to a code folder.
    """

    module_name: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Unique module name in dot delimited format."""

    def to_key(self) -> str:
        """Get Module key."""
        return 'Module=' + self.module_name

    @classmethod
    def create_key(cls, *, module_name: str) -> Union[str, ModuleKey]:
        """Create Module key."""
        return 'Module=' + module_name
