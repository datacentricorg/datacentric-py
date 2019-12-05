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
from bson import ObjectId
from typing import List, Union
from datacentric.storage.record import Record
from datacentric.storage.data_set_key import DataSetKey


@attr.s(slots=True, auto_attribs=True)
class DataSet(Record):
    """
    Dataset is a concept similar to a folder, applied to data in any
    data source including relational or document databases, OData
    endpoints, etc.

    Datasets can be stored in other datasets. The dataset where dataset
    record is stored is called parent dataset.

    Dataset has an Imports array which provides the list of TemporalIds of
    datasets where records are looked up if they are not found in the
    current dataset. The specific lookup rules are specific to the data
    source type and described in detail in the data source documentation.

    Some data source types do not support Imports. If such data
    source is used with a dataset where Imports array is not empty,
    an error will be raised.

    The root dataset uses TemporalId.Empty and does not have versions
    or its own DataSet record. It is always last in the dataset
    lookup sequence. The root dataset cannot have Imports.
    """

    data_set_name: str = attr.ib(default=None, kw_only=True)
    """Unique dataset name."""

    non_temporal: bool = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Flag indicating that the dataset is non-temporal even if the
    data source supports temporal data.

    For the data stored in datasets where NonTemporal == false, a
    temporal data source keeps permanent history of changes to each
    record within the dataset, and provides the ability to access
    the record as of the specified TemporalId, where TemporalId serves
    as a timeline (records created later have greater TemporalId than
    records created earlier).

    For the data stored in datasets where NonTemporal == true, the
    data source keeps only the latest version of the record. All
    child datasets of a non-temporal dataset must also be non-temporal.

    In a non-temporal data source, this flag is ignored as all
    datasets in such data source are non-temporal.
    """

    imports: List[ObjectId] = attr.ib(default=None, kw_only=True, repr=False, metadata={'optional': True})
    """
    List of datasets where records are looked up if they are
    not found in the current dataset.

    The specific lookup rules are specific to the data source
    type and described in detail in the data source documentation.

    The parent dataset is not included in the list of Imports by
    default and must be included in the list of Imports explicitly.
    """

    def to_key(self) -> str:
        """Get DataSet key."""
        return 'DataSet=' + self.data_set_name

    @classmethod
    def create_key(cls, *, data_set_name: str) -> Union[str, DataSetKey]:
        """Create DataSet key."""
        return 'DataSet=' + data_set_name
