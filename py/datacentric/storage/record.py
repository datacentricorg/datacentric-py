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
from abc import ABC, abstractmethod
from typing import Union, Optional, List, Any
from bson import ObjectId
from datacentric.storage.data import Data
from datacentric.storage.context import Context


@attr.s(slots=True, auto_attribs=True)
class Record(Data, ABC):
    """Base class of records stored in data source."""

    __context: Context = attr.ib(default=None, init=False)
    """Context provides platform-independent APIs for:

    * Databases and distributed cache
    * Logging and error reporting
    * Local or remote handler execution
    * Progress reporting
    * Virtualized filesystem
    """

    id_: ObjectId = attr.ib(default=None, kw_only=True)
    """
    TemporalId of the record is specific to its version.

    For the record's history to be captured correctly, all
    update operations must assign a new TemporalId with the
    timestamp that matches update time.
    """

    data_set: ObjectId = attr.ib(default=None, kw_only=True)
    """
    TemporalId of the dataset where the record is stored.

    For records stored in root dataset, the value of
    DataSet element should be TemporalId.Empty.
    """

    @property
    def context(self) -> Optional[Context]:
        """
        Execution context provides access to key resources including:

        * Logging and error reporting
        * Cloud calculation service
        * Data sources
        * Filesystem
        * Progress reporting
        """
        return self.__context

    def init(self, context: Optional[Context]) -> None:
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
    def to_key(self) -> Any:
        """
        Create key string from the current record.

        String key consists of collection name followed by the equal sign (=)
        and then semicolon delimited primary key elements:

        collection_name=key_element1;key_element2

        Collection name is the name of the class derived from Record directly.

        To avoid serialization format uncertainty, key elements
        can have any atomic type except float.
        """
        pass
