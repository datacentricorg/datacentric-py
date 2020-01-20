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

import inspect
from typing import Type, TypeVar

from datacentric.storage.data import Data
from datacentric.storage.versioning_method import VersioningMethod

TData = TypeVar('TData', bound=Data)


def versioning(cls: Type[TData] = None, *, versioning_method: VersioningMethod):
    """Records marked by Pinned attribute are always stored
    in root dataset, irrespective of the dataset specified in
    the Save method.
    """

    def wrap(_cls):
        if not inspect.isclass(_cls):
            raise Exception('@versioning should be applied on class')
        if not issubclass(_cls, Data):
            raise Exception('@versioning should be applied on Data derived class')

        _cls.versioning_method = versioning_method
        return _cls

    return wrap
