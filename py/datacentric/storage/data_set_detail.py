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

from bson import ObjectId
from typing import Optional, List
from datacentric.record.typed_key import TypedKey
from datacentric.record.typed_record import TypedRecord


class DataSetDetailKey(TypedKey['DataSetDetail']):
    """
    Provides the ability to change data associated with the dataset
    without changing the dataset record, which is immutable in a
    temporal data source.

    The reason dataset record is immutable is that any change to the
    the dataset record in a temporal data source results in creation
    of a record with new TemporalId, which is treated as a new dataset.

    The DataSetDetail record uses TemporalId of the referenced dataset
    as its primary key. It is located in the parent of the dataset
    record to which it applies, rather than inside that record, so it
    is not affected by its own settings.
    """

    __slots__ = ('data_set_id')

    data_set_id: ObjectId

    def __init__(self):
        super().__init__()

        self.data_set_id = None
        """TemporalId of the referenced dataset."""


class DataSetDetail(TypedRecord[DataSetDetailKey]):
    """
    Provides the ability to change data associated with the dataset
    without changing the dataset record, which is immutable in a
    temporal data source.

    The reason dataset record is immutable is that any change to the
    the dataset record in a temporal data source results in creation
    of a record with new TemporalId, which is treated as a new dataset.

    The DataSetDetail record uses TemporalId of the referenced dataset
    as its primary key. It is located in the parent of the dataset
    record to which it applies, rather than inside that record, so it
    is not affected by its own settings.
    """

    __slots__ = ('data_set_id', 'read_only', 'cutoff_time', 'imports_cutoff_time')

    data_set_id: ObjectId
    read_only: bool
    cutoff_time: Optional[ObjectId]
    imports_cutoff_time: Optional[ObjectId]

    def __init__(self):
        super().__init__()

        self.data_set_id = None
        """TemporalId of the referenced dataset."""

        self.read_only = None
        """
        If specified, write operations to the referenced dataset
        will result in an error.
        """

        self.cutoff_time = None
        """
        Records with TemporalId that is greater than or equal to CutoffTime
        will be ignored by load methods and queries, and the latest available
        record where TemporalId is less than CutoffTime will be returned instead.

        CutoffTime applies to both the records stored in the dataset itself,
        and the reports loaded through the Imports list.

        CutoffTime may be set in data source globally, or for a specific dataset
        in its details record. If CutoffTime is set for both, the earlier of the
        two values will be used.
        """

        self.imports_cutoff_time = None
        """
        Imported records (records loaded through the Imports list)
        where TemporalId is greater than or equal to CutoffTime
        will be ignored by load methods and queries, and the latest
        available record where TemporalId is less than CutoffTime will
        be returned instead.

        This setting only affects records loaded through the Imports
        list. It does not affect records stored in the dataset itself.

        Use this feature to freeze Imports as of a given CreatedTime
        (part of TemporalId), isolating the dataset from changes to the
        data in imported datasets that occur after that time.

        If ImportsCutoffTime is set for both data source and dataset,
        the earlier of the two values will be used.
        """
