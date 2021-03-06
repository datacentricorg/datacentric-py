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
from typing import List
from datacentric.storage.data import Data
from datacentric.schema.declaration.handler_implement_item import HandlerImplementItem


@attr.s(slots=True, auto_attribs=True)
class HandlerImplementBlock(Data):
    """
    Handler implementations are contained within this block
    in type declaration.

    TODO - we can remove this document level when switching from XML to JSON.
    """

    handlers: List[HandlerImplementItem] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """
    Each element of this list provides implementation for a
    handler that was declared in this class or its base.
    """
