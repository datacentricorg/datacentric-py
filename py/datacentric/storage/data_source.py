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
from typing import Optional, TypeVar, Iterable, List, Type
from bson import ObjectId

from datacentric.attributes.pinned_attribute import pinned
from datacentric.storage.record import Record
from datacentric.storage.data_set import DataSet
from datacentric.storage.env_type import EnvType
from datacentric.storage.context import Context
from datacentric.storage.versioning_method import VersioningMethod

TRecord = TypeVar('TRecord', bound=Record)


@attr.s(slots=True, auto_attribs=True)
@pinned
class DataSource(Record, ABC):
    """
    Data source is a logical concept similar to database
    that can be implemented for a document DB, relational DB,
    key-value store, or filesystem.

    Data source API provides the ability to:

    (a) store and query datasets;
    (b) store records in a specific dataset; and
    (c) query record across a group of datasets.

    This record is stored in root dataset.
    """

    data_source_name: str = attr.ib(default=None, kw_only=True)
    """Unique data source name."""

    env_type: EnvType = attr.ib(default=None, kw_only=True)
    """
    Environment type enumeration.

    Some API functions are restricted based on the environment type.
    """

    env_group: str = attr.ib(default=None, kw_only=True)
    """
    The meaning of environment group depends on the environment type.

    * For PROD, UAT, and DEV environment types, environment group
    identifies the endpoint.

    * For USER environment type, environment group is user alias.

    * For TEST environment type, environment group is the name of
    the unit test class (test fixture).
    """

    env_name: str = attr.ib(default=None, kw_only=True)
    """
    The meaning of environment name depends on the environment type.

    * For PROD, UAT, DEV, and USER environment types, it is the
    name of the user environment selected in the client.

    * For TEST environment type, it is the test method name.
    """

    versioning_method: VersioningMethod = attr.ib(default=None, kw_only=True)
    """Specifies the default method of record or dataset
    versioning.
    
    This value can be overridden for specific record types
    via an attribute.
    """

    read_only: bool = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Use this flag to mark data source as readonly.

    Data source may also be readonly because CutoffTime is set.
    """

    # --- METHODS

    def init(self, context: Context) -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method may be called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        IMPORTANT - Every override of this method must call base.Init()
        first, and only then execute the rest of the override method's code.
        """

        # Initialize base before executing the rest of the code in this method
        super().init(context)

        # Perform database name validation
        if not self.env_type or self.env_type == EnvType.Empty:
            raise Exception('Data source environment type is not specified.')
        if not self.env_group:
            raise Exception('Data source environment group is not specified.')
        if not self.env_name:
            raise Exception('Data source environment name is not specified.')

    def to_key(self) -> str:
        """Get DataSource key."""
        return 'DataSource=' + self.data_source_name

    # --- CLASS

    @classmethod
    def create_key(cls, *, data_source_name: str) -> str:
        """Create DataSource key."""
        return 'DataSource=' + data_source_name

    # --- METHODS

    @abstractmethod
    def create_ordered_object_id(self) -> ObjectId:
        """The returned ObjectIds have the following order guarantees:

        * For this data source instance, to arbitrary resolution; and
        * Across all processes and machines, to one second resolution

        One second resolution means that two ObjectIds created within
        the same second by different instances of the data source
        class may not be ordered chronologically unless they are at
        least one second apart."""
        pass

    @abstractmethod
    def load_or_null(self, record_type: Type[TRecord], id_: ObjectId) -> Optional[TRecord]:
        """Load record by its ObjectId.

        Return None if there is no record for the specified ObjectId;
        however an exception will be thrown if the record exists but
        is not derived from type_.
        """
        pass

    @abstractmethod
    def load_or_null_by_key(self, record_type: Type[TRecord], key_: str, load_from: ObjectId) -> Optional[TRecord]:
        """Load record by string key from the specified dataset or
        its list of imports. The lookup occurs first in descending
        order of dataset ObjectIds, and then in the descending
        order of record ObjectIds within the first dataset that
        has at least one record. Both dataset and record ObjectIds
        are ordered chronologically to one second resolution,
        and are unique within the database server or cluster.

        The root dataset has empty ObjectId value that is less
        than any other ObjectId value. Accordingly, the root
        dataset is the last one in the lookup order of datasets.

        The first record in this lookup order is returned, or null
        if no records are found or if DeletedRecord is the first
        record.

        Return None if there is no record for the specified ObjectId;
        however an exception will be thrown if the record exists but
        is not derived from TRecord.
        """
        pass

    @abstractmethod
    def get_query(self, record_type: Type[TRecord], load_from: ObjectId):
        """Get query for the specified type.

        After applying query parameters, the lookup occurs first in
        descending order of dataset ObjectIds, and then in the descending
        order of record ObjectIds within the first dataset that
        has at least one record. Both dataset and record ObjectIds
        are ordered chronologically to one second resolution,
        and are unique within the database server or cluster.

        The root dataset has empty ObjectId value that is less
        than any other ObjectId value. Accordingly, the root
        dataset is the last one in the lookup order of datasets.
        """
        pass

    @abstractmethod
    def save_many(self, record_type: Type[TRecord], records: Iterable[TRecord], save_to: ObjectId) -> None:
        """Save multiple records to the specified dataset. After the method exits,
        for each record the property record.data_set will be set to the value of
        the save_to parameter.

        All save methods ignore the value of record.data_set before the
        save method is called. When dataset is not specified explicitly,
        the value of dataset from the context, not from the record, is used.
        The reason for this behavior is that the record may be stored from
        a different dataset than the one where it is used.

        This method guarantees that ObjectIds of the saved records will be in
        strictly increasing order.
        """
        pass

    @abstractmethod
    def delete(self, record_type: Type[TRecord], key: str, delete_in: ObjectId) -> None:
        """Write a DeletedRecord in delete_in dataset for the specified key
        instead of actually deleting the record. This ensures that
        a record in another dataset does not become visible during
        lookup in a sequence of datasets.

        To avoid an additional roundtrip to the data store, the delete
        marker is written even when the record does not exist.
        """
        pass

    @abstractmethod
    def delete_db(self) -> None:
        """Permanently deletes (drops) the database with all records
        in it without the possibility to recover them later.

        This method should only be used to free storage. For
        all other purposes, methods that preserve history should
        be used.

        ATTENTION - THIS METHOD WILL DELETE ALL DATA WITHOUT
        THE POSSIBILITY OF RECOVERY. USE WITH CAUTION.
        """
        pass

    @abstractmethod
    def get_data_set_or_none(self, data_set_name: str) -> Optional[ObjectId]:
        """Get ObjectId of the dataset with the specified name.
        Returns null if not found.
        """
        pass

    @abstractmethod
    def save_data_set(self, data_set: DataSet) -> None:
        """Save new version of the dataset and update in-memory cache to the saved dataset."""
        pass

    # From extensions:
    def load(self, record_type: Type[TRecord], id_: ObjectId) -> TRecord:
        """Load record by its ObjectId.

        Error message if there is no record for the specified ObjectId,
        or if the record exists but is not derived from record_type.
        """
        raise NotImplementedError()

    def load_by_key(self, record_type: Type[TRecord], key_, load_from: ObjectId) -> TRecord:
        """Load record from context.data_source, overriding the dataset
        specified in the context with the value specified as the
        second parameter. The lookup occurs in the specified dataset
        and its imports, expanded to arbitrary depth with repetitions
        and cyclic references removed.

        IMPORTANT - this overload of the method loads from load_from
        dataset, not from context.data_set.

        Error message if the record is not found or is a DeletedRecord.
        """
        result = self.load_or_null_by_key(record_type, key_, load_from)
        if result is None:
            raise Exception(f'Record with key {key_} is not found in dataset with TemporalId={load_from}.')
        return result

    def save_one(self, record_type: Type[TRecord], record: TRecord, save_to: ObjectId):
        """Save one record to the specified dataset. After the method exits,
        record.data_set will be set to the value of the data_set parameter.

        All save methods ignore the value of record.data_set before the
        Save method is called. When dataset is not specified explicitly,
        the value of dataset from the context, not from the record, is used.
        The reason for this behavior is that the record may be stored from
        a different dataset than the one where it is used.

        This method guarantees that ObjectIds of the saved records will be in
        strictly increasing order.
        """
        self.save_many(record_type, [record], save_to)

    def get_data_set(self, data_set_name: str) -> ObjectId:
        """Get ObjectId of the dataset with the specified name.
        Error message if not found.
        """
        result = self.get_data_set_or_none(data_set_name)
        if result is None:
            raise Exception(f'Dataset {data_set_name} is not found in data store {self.data_source_name}.')
        return result

    def create_data_set(self, data_set_name: str, imports: List[ObjectId] = None) -> ObjectId:
        """Create dataset with the specified data_set_name, parent_data_set, imports,
        and flags.

        This method updates in-memory dataset cache to include
        the created dataset.
        """

        # Make None if either None or empty
        if imports is None:
            imports = []
        if len(imports) == 0:
            imports = None

        result = DataSet()
        result.data_set_name = data_set_name
        result.imports = imports

        self.save_data_set(result)

        return result.id_
