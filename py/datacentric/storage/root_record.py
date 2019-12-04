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
from bson import ObjectId

from datacentric.storage.context import Context
from datacentric.storage.record import Record


@attr.s(slots=True)
class RootRecord(Record, ABC):
    """
    Base class of records stored in root dataset of the data store.

    init(...) method of this class sets data_set to temporal_id.empty.
    """

    def init(self, context: Context) -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method must work when called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        All overrides of this method must call base.Init(context) first, then
        execute the rest of the code in the override.
        """

        # Initialize base before executing the rest of the code in this method
        super().init(context)

        # For this base type of records stored in root dataset,
        # set data_set element to the value designated for the
        # root dataset: temporal_id.empty.
        self.data_set = ObjectId('000000000000000000000000')
