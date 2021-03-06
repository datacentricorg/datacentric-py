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
from typing import Dict, Optional, TypeVar, Set, Iterable, Type
from bson import ObjectId
from pymongo.collection import Collection
from datacentric.storage.mongo.temporal_mongo_query import TemporalMongoQuery
from datacentric.storage.record import Record
from datacentric.storage.deleted_record import DeletedRecord
from datacentric.storage.data_set import DataSet
from datacentric.storage.data_source import DataSource
from datacentric.storage.mongo.mongo_data_source import MongoDataSource
from datacentric.storage.class_info import ClassInfo
from datacentric.serialization.serializer import serialize, deserialize
from bson.codec_options import DEFAULT_CODEC_OPTIONS

from datacentric.storage.temporal_id import empty_id
from datacentric.storage.versioning_method import VersioningMethod

TRecord = TypeVar('TRecord', bound=Record)


@attr.s(slots=True, auto_attribs=True)
class TemporalMongoDataSource(MongoDataSource):
    """
    Temporal data source with datasets based on MongoDB.

    The term Temporal applied means the data source stores complete revision
    history including copies of all previous versions of each record.

    In addition to being temporal, this data source is also hierarchical; the
    records are looked up across a hierarchy of datasets, including the dataset
    itself, its direct Imports, Imports of Imports, etc., ordered by dataset's
    TemporalId.
    """

    cutoff_time: ObjectId = attr.ib(default=None, kw_only=True, metadata={'optional': True})
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

    __collection_dict: Dict[type, Collection] = attr.ib(factory=dict, init=False)
    __data_set_dict: Dict[str, ObjectId] = attr.ib(factory=dict, init=False)
    __import_dict: Dict[ObjectId, Set[ObjectId]] = attr.ib(factory=dict, init=False)

    __codec_options = DEFAULT_CODEC_OPTIONS.with_options(tz_aware=True)
    """
    By default, UTC datetime is imported by PyMongo as timezone naive.
    This setting changes that. This variable is used as argument for
    get_collection(...).
    """

    def load(self, record_type: Type[TRecord], id_: ObjectId) -> TRecord:
        raise NotImplemented

    def load_or_null(self, record_type: Type[TRecord], id_: ObjectId) -> Optional[TRecord]:
        """Load record by its ObjectId.

        Return None if if argument ObjectId is greater than
        or equal to CutoffTime.
        """
        if self.cutoff_time is not None:
            if id_ >= self.cutoff_time:
                return None

        pipeline = [
            {'$match': {'_id': {'$eq': id_}}},
            {'$limit': 1}
        ]
        collection = self._get_or_create_collection(record_type)
        cursor = collection.aggregate(pipeline)
        if cursor.alive:
            cursor_next = cursor.next()
            result: TRecord = deserialize(cursor_next)

            if result is not None and not isinstance(result, DeletedRecord):

                is_requested_instance = isinstance(result, record_type)
                if not is_requested_instance:
                    raise Exception(f'Stored type {type(result).__name__} for ObjectId={id_} and '
                                    f'Key={result.to_key()} is not an instance of the requested type '
                                    f'{record_type.__name__}.')
                result.init(self.context)
                return result
        return None

    def load_or_null_by_key(self, type_: Type[TRecord], key_: str, load_from: ObjectId) -> Optional[TRecord]:
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
        collection_name, key_value = key_.split('=', 1)

        base_pipe = [{"$match": {"_key": key_value}}]
        pipe_with_constraints = self.apply_final_constraints(base_pipe, load_from)
        ordered_pipe = pipe_with_constraints
        ordered_pipe.extend(
            [
                {"$sort": {"_dataset": -1}},
                {"$sort": {"_id": -1}},
                {'$limit': 1}
            ]
        )

        collection = self._get_or_create_collection(type_)

        cursor = collection.aggregate(ordered_pipe)
        if cursor.alive:
            cursor_next = cursor.next()
            result: TRecord = deserialize(cursor_next)

            if result is not None and not isinstance(result, DeletedRecord):

                is_proper_record = isinstance(result, type_)
                if not is_proper_record:
                    raise Exception(f'Stored type {type(result).__name__} for Key={key_} in '
                                    f'data_set={load_from} is not an instance of '
                                    f'the requested type {type_.__name__}.')
                result.init(self.context)
                return result
        return None

    def get_query(self, record_type: Type[TRecord], load_from: ObjectId) -> TemporalMongoQuery:
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
        collection = self._get_or_create_collection(record_type)
        return TemporalMongoQuery(record_type, self, collection, load_from)

    def save_many(self, record_type: Type[TRecord], records: Iterable[TRecord], save_to: ObjectId):
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
        self._check_not_readonly()

        collection = self._get_or_create_collection(record_type)
        if records is None:
            return None

        for record in records:
            record_id = self.create_ordered_object_id()
            if record_id <= save_to:
                raise Exception(f'TemporalId={record_id} of a record must be greater than '
                                f'TemporalId={save_to} of the dataset where it is being saved.')
            record.id_ = record_id
            record.data_set = save_to
            record.init(self.context)

        versioning_method = self.get_versioning_method(record_type)
        if versioning_method == VersioningMethod.Temporal:
            collection.insert_many([serialize(x) for x in records])
        elif (versioning_method == VersioningMethod.NonTemporal) or (
                versioning_method == VersioningMethod.NonOverriding):
            collection.insert_many([serialize(x) for x in records])  # TODO: replace by upsert
        else:
            raise Exception(f'Unknown versioning method {versioning_method}.')

    def delete(self, record_type: Type[TRecord], key: str, delete_in: ObjectId) -> None:
        """Write a DeletedRecord in delete_in dataset for the specified key
        instead of actually deleting the record. This ensures that
        a record in another dataset does not become visible during
        lookup in a sequence of datasets.

        To avoid an additional roundtrip to the data store, the delete
        marker is written even when the record does not exist.
        """
        self._check_not_readonly()

        record = DeletedRecord()
        record.key = key

        record.id_ = self.create_ordered_object_id()
        record.data_set = delete_in

        collection = self._get_or_create_collection(record_type)

        collection.insert_one(record)

    def apply_final_constraints(self, pipeline, load_from: ObjectId):
        """Apply the final constraints after all prior where clauses but before sort_by clause:

        * The constraint on dataset lookup list, restricted by cutoff_time (if not none)
        * The constraint on ID being strictly less than cutoff_time (if not none).
        """
        data_set_lookup_list = self.get_data_set_lookup_list(load_from)
        pipeline.append({'$match': {"_dataset": {"$in": list(data_set_lookup_list)}}})

        if self.cutoff_time is not None:
            pipeline.append({'$match': {'_id': {'$lte': self.cutoff_time}}})

        return pipeline

    def get_data_set_or_none(self, data_set_name: str) -> Optional[ObjectId]:
        """Get ObjectId of the dataset with the specified name.
        Returns null if not found.
        """
        if data_set_name in self.__data_set_dict:
            return self.__data_set_dict[data_set_name]

        data_set_record = self.load_or_null_by_key(DataSet, DataSet.create_key(data_set_name=data_set_name), empty_id)

        if data_set_record is None:
            return None

        self.__data_set_dict[data_set_name] = data_set_record.id_

        if data_set_record.id_ not in self.__import_dict:
            import_set = self._build_data_set_lookup_list(data_set_record)
            self.__import_dict[data_set_record.id_] = import_set

        return data_set_record.id_

    def save_data_set(self, data_set: DataSet) -> None:
        """Save new version of the dataset and update in-memory cache to the saved dataset."""
        self.save_one(DataSet, data_set, empty_id)
        self.__data_set_dict[data_set.to_key()] = data_set.id_

        lookup_set = self._build_data_set_lookup_list(data_set)
        self.__import_dict[data_set.id_] = lookup_set

    def get_data_set_lookup_list(self, load_from: ObjectId) -> Iterable[ObjectId]:
        """Returns enumeration of import datasets for specified dataset data,
        including imports of imports to unlimited depth with cyclic
        references and duplicates removed.
        """
        if load_from == empty_id:
            return [empty_id]

        if load_from in self.__import_dict:
            return self.__import_dict[load_from]

        else:
            data_set_data: DataSet = self.load_or_null(DataSet, load_from)
            if data_set_data is None:
                raise Exception(f'Dataset with ObjectId={load_from} is not found.')
            if data_set_data.data_set != empty_id:
                raise Exception(f'Dataset with ObjectId={load_from} is not stored in root dataset.')
            result = self._build_data_set_lookup_list(data_set_data)
            self.__import_dict[load_from] = result
            return result

    def get_versioning_method(self, record_type: Type[TRecord]) -> VersioningMethod:
        """Gets the method of record or dataset versioning.

        Versioning method is a required field for the data source. Its
        value can be overridden for specific record types via an attribute.
        """
        if hasattr(record_type, 'versioning_method'):
            return getattr(record_type, 'versioning_method')

        return self.versioning_method

    def is_pinned(self, record_type: Type[TRecord]) -> bool:
        """Returns true if the record has Pinned attribute."""
        if hasattr(record_type, 'is_pinned') and getattr(record_type, 'is_pinned'):
            return True

        return False

    def get_imports_cutoff_time(self, data_set_id: ObjectId) -> Optional[ObjectId]:
        """Gets ImportsCutoffTime from the dataset detail record.
        Returns None if dataset detail record is not found.

        Imported records (records loaded through the imports list)
        where ObjectId is greater than or equal to cutoff_time
        will be ignored by load methods and queries, and the latest
        available record where ObjectId is less than cutoff_time will
        be returned instead.

        This setting only affects records loaded through the imports
        list. It does not affect records stored in the dataset itself.

        Use this feature to freeze imports as of a given created time
        (part of ObjectId), isolating the dataset from changes to the
        data in imported datasets that occur after that time.
        """

        # TODO: implement when stored in dataset
        return None

    def _get_or_create_collection(self, type_: type) -> Collection:
        if type_ in self.__collection_dict:
            return self.__collection_dict[type_]
        root_type = ClassInfo.get_ultimate_base(type_)
        collection_name = root_type.__name__
        collection = self.db.get_collection(collection_name, self.__codec_options)
        self.__collection_dict[type_] = collection
        return collection

    def _build_data_set_lookup_list(self, data_set_record: DataSet) -> Set[ObjectId]:
        result: Set[ObjectId] = set()

        self._fill_data_set_lookup_set(data_set_record, result)

        return result

    def _fill_data_set_lookup_set(self, data_set_record: DataSet, result: Set[ObjectId]) -> None:
        if data_set_record is None:
            return

        if not ObjectId.is_valid(data_set_record.id_):
            raise Exception('Required ObjectId value is not set.')
        if data_set_record.data_set_name == '':
            raise Exception('Required string value is not set.')

        if self.cutoff_time is not None and data_set_record.id_ >= self.cutoff_time:
            return

        result.add(data_set_record.id_)

        if data_set_record.imports is not None:
            for data_set_id in data_set_record.imports:
                if data_set_record.id_ == data_set_id:
                    raise Exception(f'Dataset {data_set_record.to_key()} with ObjectId={data_set_record.id_} '
                                    f'includes itself in the list of its imports.')
                if data_set_id not in result:
                    result.add(data_set_id)
                    cached_import_list = self.get_data_set_lookup_list(data_set_id)
                    for import_id in cached_import_list:
                        result.add(import_id)

    def _check_not_readonly(self):
        """Error message if either ReadOnly flag or CutoffTime is set
        for the data source."""
        if self.read_only:
            raise Exception(f'Attempting write operation for data source {self.data_source_name} '
                            f'where ReadOnly flag is set.')

        if self.cutoff_time is not None:
            raise Exception(f'Attempting write operation for data source {self.data_source_name} where '
                            f'CutoffTime is set. Historical view of the data cannot be written to.')
