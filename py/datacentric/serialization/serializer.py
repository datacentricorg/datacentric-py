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
import datetime as dt
from bson import ObjectId, Int64
from enum import IntEnum
from typing import Dict, Any, TypeVar, List
from typing_inspect import get_origin, get_args
from datacentric.primitive.string_util import StringUtil
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.class_info import ClassInfo
from datacentric.storage.record import Record
from datacentric.storage.data import Data

TRecord = TypeVar('TRecord', bound=Record)


# Serialization: object -> dict

# TODO: Refactor
def serialize(obj: TRecord) -> Dict[str, Any]:
    type_: type = type(obj)
    dict_ = _serialize_class(obj, type_)

    # Field _t contains inheritance chain of the class, starting from Record
    dict_['_t'] = ClassInfo.get_inheritance_chain(type_)

    # ObjectId of the dataset
    dict_['_dataset'] = obj.data_set

    # Remove collection name prefix from key before assigning
    key_with_collection_name_prefix: str = obj.to_key()
    key_without_collection_name_prefix: str = key_with_collection_name_prefix.split('=', 1)[1]
    dict_['_key'] = key_without_collection_name_prefix

    # Unique object id
    dict_['_id'] = obj.id_

    return dict_


def _serialize_class(obj: TRecord, expected_: type) -> Dict[str, Any]:
    dict_: Dict[str, Any] = dict()

    cls_type = type(obj)
    # Check that object has expected type
    if cls_type != expected_:
        raise Exception(f'Expected: {expected_.__name__}, actual: {cls_type.__name__}')

    # Field _t contains inheritance chain of the class, starting from Record
    dict_['_t'] = ClassInfo.get_inheritance_chain(cls_type)

    fields = attr.fields(cls_type)

    mro = cls_type.__mro__
    if Record in mro:
        serializable_fields = [x for x in fields if x not in attr.fields(Record)]
    elif Data in mro:
        serializable_fields = [x for x in fields if x not in attr.fields(Data)]
    else:
        raise Exception(f'Cannot serialize class {cls_type.__name__} not derived from Record or Data.')

    non_private_fields = [x for x in serializable_fields if not x.name.startswith('_')]

    for field in non_private_fields:  # type: attr.Attribute
        value = getattr(obj, field.name)

        expected_type = field.type

        is_optional = field.metadata.get('optional', False)
        is_list = get_origin(expected_type) is not None and get_origin(expected_type) is list

        if value is None:
            if not is_optional and not is_list:
                raise Exception(f'Missing required field: {field.name} in type: {cls_type.__name__}')
            continue

        serialized_value: Any
        if is_list:
            expected_arg = get_args(expected_type)[0]
            serialized_value = _serialize_list(value, expected_arg, field.metadata)

        elif issubclass(expected_type, Data):
            serialized_value = _serialize_class(value, expected_type)
        elif issubclass(expected_type, IntEnum):
            serialized_value = _serialize_enum(value)
        else:
            serialized_value = _serialize_primitive(value, expected_type, field.metadata)

        dict_[StringUtil.to_pascal_case(field.name)] = serialized_value
    return dict_


def _serialize_list(list_, expected_, meta_: Dict[Any, Any]) -> List[Any]:
    is_optional = meta_.get('optional', False)
    is_required = not is_optional
    if is_required and None in list_:
        Exception('Lists not marked as optional cannot contain None elements.')

    if issubclass(expected_, Data):
        return [_serialize_class(x, expected_) for x in list_]
    elif issubclass(expected_, IntEnum):
        return [_serialize_enum(x) for x in list_]
    else:
        return [_serialize_primitive(x, expected_, meta_) for x in list_]


def _serialize_enum(value_: IntEnum):
    if issubclass(type(value_), IntEnum):
        return value_.name
    else:
        raise Exception(f'Expected subclass of IntEnum, got {type(value_)}')


def _serialize_primitive(value, expected_, meta_: Dict[Any, Any]):
    # The only case to have None here -> List with optional in metadata
    if value is None:
        return None

    value_type = type(value)
    if value_type != expected_:
        raise Exception(f'Expected {expected_.__name__}, got {value_type.__name__}')

    has_type = 'type' in meta_
    is_key = 'key' in meta_

    # Check that expected collection name is equal to actual
    if is_key:
        collection_in_key = value.split('=', 1)[0]
        collection_in_metadata = meta_.get('key')
        if collection_in_key != collection_in_metadata:
            raise Exception(f'Wrong key: expected: {collection_in_metadata}, got: {collection_in_key}.')
        return value

    if has_type:
        type_hint = meta_.get('type')
        if type_hint == 'LocalDate':
            if 19700101 <= value <= 99991231:
                return value
            else:
                raise Exception(f'Wrong value for local date: {value}')

        if type_hint == 'LocalTime':
            if 0 <= value <= 235959999:
                return value
            else:
                raise Exception(f'Wrong value for local time: {value}')

        if type_hint == 'LocalMinute':
            if 0 <= value <= 2359:
                return value
            else:
                raise Exception(f'Wrong value for local minute: {value}')

        if type_hint == 'LocalDateTime':
            if 19700101000000000 <= value <= 99991231235959999:
                return value
            else:
                raise Exception(f'Wrong value for local date_time: {value}')

        # TODO: define check for instant
        if type_hint == 'Instant':
            return value

        if type_hint == 'long':
            return value
        raise Exception(f'Cannot resolve metadata type: {type_hint}.')

    if value_type == dt.datetime:
        return LocalDateTime.from_datetime(value)
    elif value_type == dt.date:
        return LocalDate.from_date(value)
    elif value_type == dt.time:
        return LocalTime.from_time(value)
    elif value_type == str:
        return value
    elif value_type == bool:
        return value
    elif value_type == int:
        return value
    elif value_type == float:
        return value
    elif value_type == ObjectId:
        return value
    else:
        raise Exception(f'Cannot serialize type {value_type.__name__}')


# Deserialization: dict -> object

# TODO: Refactor
def deserialize(dict_: Dict[str, Any]) -> TRecord:
    # key_ is omitted and is calculated using records to_
    dict_.pop('_key')

    data_set = dict_.pop('_dataset')
    id_ = dict_.pop('_id')

    new_obj: TRecord = _deserialize_class(dict_)

    setattr(new_obj, 'data_set', data_set)
    setattr(new_obj, 'id_', id_)

    return new_obj


def _deserialize_class(dict_: Dict[str, Any]) -> TRecord:
    type_name: str = dict_.pop('_t')[-1]

    type_info: type = ClassInfo.get_type(type_name)

    fields = attr.fields_dict(type_info)
    new_obj = type_info()

    for dict_key, dict_value in dict_.items():
        slot = StringUtil.to_snake_case(dict_key)

        field = fields[slot]
        member_type = field.type

        deserialized_value: Any
        if get_origin(member_type) is not None and get_origin(member_type) is list:
            deserialized_value = _deserialize_list(member_type, dict_value, field.metadata)
        elif issubclass(member_type, Data):
            deserialized_value = _deserialize_class(dict_value)
        elif issubclass(member_type, IntEnum):
            deserialized_value = member_type[dict_value]
        else:
            deserialized_value = _deserialize_primitive(member_type, dict_value, field.metadata)

        setattr(new_obj, slot, deserialized_value)
    return new_obj


def _deserialize_list(type_: type, list_, meta_: Dict[Any, Any]) -> List[Any]:
    expected_item_type = get_args(type_)[0]

    if issubclass(expected_item_type, Data):
        return [_deserialize_class(x) for x in list_]
    elif issubclass(expected_item_type, IntEnum):
        return [expected_item_type[x] for x in list_]
    elif expected_item_type is list:
        raise Exception(f'List of lists are prohibited.')
    else:
        return [_deserialize_primitive(expected_item_type, x, meta_) for x in list_]


def _deserialize_primitive(expected_type, value, meta_: Dict[Any, Any]):
    is_key = 'key' in meta_
    has_type = 'type' in meta_
    value_type = type(value)

    if has_type:
        meta_type = meta_.get('type')
        if value_type == expected_type:
            return value
        elif meta_type == 'LocalDateTime' and value_type == Int64:
            return value
        elif meta_type == 'long' and value_type == Int64:
            return value
        else:
            raise Exception(f'Unknown case for metadata type: {meta_type}. Actual: {value_type.__name__}')

    # Additional cases for date classes
    if value_type != expected_type:
        if value_type == int and expected_type == dt.time:
            return LocalTime.to_time(value)
        elif value_type == int and expected_type == dt.date:
            return LocalDate.to_date(value)
        elif value_type == Int64 and expected_type == dt.datetime:
            return LocalDateTime.to_datetime(value)
        elif meta_.get('optional', False) and value is None:
            return None
        else:
            raise Exception(f'Expected {expected_type.__name__}, got {value_type.__name__}')

    # Case for key and key check
    if is_key:
        collection_in_key = value.split('=', 1)[0]
        collection_in_metadata = meta_.get('key')
        if collection_in_key != collection_in_metadata:
            raise Exception(f'Wrong key: expected: {collection_in_metadata}, got: {collection_in_key}.')
        return value

    # Primitives
    if expected_type == str:
        return value
    elif expected_type == bool:
        return value
    elif expected_type == int:
        return value
    elif expected_type == float:
        return value
    elif expected_type == ObjectId:
        return value
    else:
        raise Exception(f'Cannot deduce type {expected_type}')
