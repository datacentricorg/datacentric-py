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

from abc import ABC, abstractmethod
from bson import ObjectId
from datacentric.storage.data import Data

# To prevent linter error on type hint in quotes
if False:
    from datacentric.storage.context import Context


class Record(Data, ABC):
    """Base class of records stored in data source."""

    __slots__ = ('__context', 'id_', 'data_set', '_key')

    __context: 'Context'
    id_: ObjectId
    data_set: ObjectId
    _key: str

    def __init__(self):
        super().__init__()

        self.__context = None
        """
        Execution context provides access to key resources including:

        * Logging and error reporting
        * Cloud calculation service
        * Data sources
        * Filesystem
        * Progress reporting
        """

        self.id_ = None
        """
        TemporalId of the record is specific to its version.

        For the record's history to be captured correctly, all
        update operations must assign a new TemporalId with the
        timestamp that matches update time.
        """

        self.data_set = None
        """
        TemporalId of the dataset where the record is stored.

        For records stored in root dataset, the value of
        DataSet element should be TemporalId.Empty.
        """

        self._key = None
        """
        String key consists of semicolon delimited primary key elements:

        KeyElement1;KeyElement2

        To avoid serialization format uncertainty, key elements
        can have any atomic type except float.
        """

    @property
    def context(self) -> 'Context':
        """
        Execution context provides access to key resources including:

        * Logging and error reporting
        * Cloud calculation service
        * Data sources
        * Filesystem
        * Progress reporting
        """
        return self.__context

    def init(self, context: 'Context') -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method may be called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        IMPORTANT - Every override of this method must call base.Init()
        first, and only then execute the rest of the override method's code.
        """
        if context is None:
            raise Exception(
                f"Null context is passed to the Init(...) method for {type(self).__name__}.")
        self.__context = context

    @property
    @abstractmethod
    def key(self) -> str:
        """String key consists of semicolon delimited primary key elements:

        key_element1;key_element2

        To avoid serialization format uncertainty, key elements
        can have any atomic type except float.
        """
        pass
