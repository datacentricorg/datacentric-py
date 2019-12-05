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
import numpy as np
import datetime as dt
from bson import ObjectId
from enum import IntEnum
from typing import Dict, Any, get_type_hints, TypeVar, Union, List
from typing_inspect import get_origin, get_args
from datacentric.primitive.string_util import StringUtil
from datacentric.storage.class_info import ClassInfo
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.date_time.instant import Instant
from datacentric.storage.key import Key
from datacentric.storage.record import Record
from datacentric.storage.data import Data

TRecord = TypeVar('TRecord', bound=Record)

_local_hints_ = [LocalMinute, LocalDateTime, LocalDate, LocalTime]


# Serialization: object -> dict

# TODO: Refactor
def serialize(obj: TRecord):
    type_: type = type(obj)
    dict_ = _serialize_class(obj, type_)

    # Field _t contains inheritance chain of the class, starting from Record
    dict_['_t'] = ClassInfo.get_record_inheritance_chain(type_)

    # ObjectId of the dataset
    dict_['_dataset'] = obj.data_set

    # Remove collection name prefix from key before assigning
    key_with_collection_name_prefix: str = obj.to_key()
    key_without_collection_name_prefix: str = key_with_collection_name_prefix.split('=', 1)[1]
    dict_['_key'] = key_without_collection_name_prefix

    # Unique object id
    dict_['_id'] = obj.id_

    return dict_


def _serialize_class(obj: TRecord, expected_: type):
    dict_: Dict[str, Any] = dict()

    cls_type = type(obj)
    # Check that object has expected type
    if cls_type != expected_:
        raise Exception(f'Expected: {expected_.__name__}, actual: {cls_type.__name__}')

    cls_name = cls_type.__name__
    dict_['_t'] = cls_name

    mro = cls_type.__mro__
    fields = attr.fields(cls_type)

    if Record in mro:
        serializable_fields = [x for x in fields if x not in attr.fields(Record)]
    elif Data in mro:
        serializable_fields = [x for x in fields if x not in attr.fields(Data)]
    else:
        raise Exception(f'Cannot serialize class {cls_name} not derived from Record or Data.')

    non_private_fields = [x for x in serializable_fields if not x.name.startswith('_')]

    field: attr.Attribute
    for field in non_private_fields:
        value = getattr(obj, field.name)
        expected_type = field.type

        is_optional = field.metadata.get('optional', False)
        is_list = get_origin(expected_type) is not None and get_origin(expected_type) is list
        is_union = get_origin(expected_type) is not None and get_origin(expected_type) is Union

        if value is None:
            if not is_optional and not is_list:
                raise Exception(f'Missing required field: {field.name} in type: {cls_name}')
            continue

        if is_union:
            serialized_value = _serialize_unions(expected_type, value)

        elif is_list:
            expected_arg = get_args(expected_type)[0]
            serialized_value = _serialize_list(value, expected_arg, is_optional)

        elif issubclass(expected_type, Data):
            serialized_value = _serialize_class(value, expected_type)
        elif issubclass(expected_type, IntEnum):
            serialized_value = _serialize_enum(value)
        else:
            serialized_value = _serialize_primitive(value, expected_type)

        dict_[StringUtil.to_pascal_case(field.name)] = serialized_value
    return dict_


def _serialize_unions(type_hint, value_) -> Any:
    args = get_args(type_hint)

    if args[0] is str and issubclass(args[1], Key):
        if type(value_) is not str:
            raise Exception(f'Expected str')
        return value_
    if args[0] is int and args[1] in _local_hints_:
        if type(value_) is not int:
            raise Exception(f'Expected int')  # TODO Improve comment to be specific about which date type is used
        return value_
    if args[0] is dt.datetime and args[1] == Instant:
        if type(value_) is not dt.datetime:
            raise Exception(f'Expected dt.datetime')
        return value_
    raise Exception(f'Unexpected Union arguments: {args}')


def _serialize_list(list_, expected_, is_optional: bool) -> List[Any]:
    is_required = not is_optional
    if is_required and None in list_:
        Exception('Lists not marked as optional cannot contain None elements.')
    is_union = get_origin(expected_) is not None and get_origin(expected_) is Union

    if is_union:
        return [_serialize_unions(expected_, x) for x in list_]
    elif issubclass(expected_, Data):
        return [_serialize_class(x, expected_) for x in list_]
    elif issubclass(expected_, IntEnum):
        return [_serialize_enum(x) for x in list_]
    else:
        return [_serialize_primitive(x, expected_) for x in list_]


def _serialize_enum(value_: IntEnum):
    if issubclass(type(value_), IntEnum):
        return value_.name
    else:
        raise Exception(f'Expected subclass of IntEnum, got {type(value_)}')


def _serialize_key(value_: Key):
    if issubclass(type(value_), Key):
        return value_.value
    else:
        raise Exception(f'Expected subclass of Key, got {type(value_)}')


def _serialize_primitive(value, expected_):
    # The only case to have None here -> List with optional in metadata
    if value is None:
        return None

    value_type = type(value)
    if value_type != expected_:
        raise Exception(f'Expected {expected_.__name__}, got {value_type.__name__}')

    if value_type == LocalMinute:
        return value.to_iso_int()
    if value_type == LocalTime:
        return value.to_iso_int()
    if value_type == LocalDate:
        return value.to_iso_int()
    if value_type == LocalDateTime:
        return value.to_iso_int()
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
def deserialize(dict_: Dict) -> TRecord:
    data_set = dict_.pop('_dataset')
    _key = dict_.pop('_key')
    id_ = dict_.pop('_id')

    new_obj: TRecord = _deserialize_class(dict_)

    new_obj.__setattr__('data_set', data_set)
    # new_obj.__setattr__('_key', _key)
    new_obj.__setattr__('id_', id_)

    return new_obj


def _deserialize_class(dict_: Dict[str, Any]) -> TRecord:
    type_name: str = dict_.pop('_t')[-1]

    type_info = ClassInfo.get_type(type_name)

    hints = get_type_hints(type_info)
    new_obj = type_info()

    for dict_key, dict_value in dict_.items():
        slot = StringUtil.to_snake_case(dict_key)

        member_type = hints[slot]

        # Resolve Optional[Type] case
        if get_origin(member_type) is not None and get_origin(member_type) is Union:
            union_args = get_args(member_type)
            if union_args[1] is type(None):
                member_type = union_args[0]

        if get_origin(member_type) is not None and get_origin(member_type) is list:
            deserialized_value = _deserialize_list(member_type, dict_value)
        elif get_origin(member_type) is not None and get_origin(member_type) is Union:
            deserialized_value = dict_value
        elif issubclass(member_type, Key):
            deserialized_value = member_type()
            deserialized_value.populate_from_string(dict_value)
        elif issubclass(member_type, Data):
            deserialized_value = _deserialize_class(dict_value)
        elif issubclass(member_type, IntEnum):
            deserialized_value = member_type[dict_value]
        else:
            deserialized_value = _deserialize_primitive(member_type, dict_value)

        new_obj.__setattr__(slot, deserialized_value)
    return new_obj


def _deserialize_list(type_: type, list_):
    expected_item_type = get_args(type_)[0]
    origin = get_origin(expected_item_type)
    if origin is not None and origin is Union:
        return list_
    if issubclass(expected_item_type, Key):
        result = []
        for item in list_:
            deserialized_key = expected_item_type()
            deserialized_key.populate_from_string(item)
            result.append(deserialized_key)
        return result
    elif issubclass(expected_item_type, Data):
        return [_deserialize_class(x) for x in list_]
    elif issubclass(expected_item_type, IntEnum):
        return [expected_item_type[x] for x in list_]
    elif expected_item_type is list:
        raise Exception(f'List of lists are prohibited.')
    else:
        return [_deserialize_primitive(expected_item_type, x) for x in list_]


def _deserialize_primitive(expected_type, value):
    if expected_type == str:
        return value
    elif expected_type == np.ndarray:
        return np.array(value)
    elif expected_type == bool:
        return value
    elif expected_type == LocalMinute:
        return LocalMinute.from_iso_int(value)
    elif expected_type == LocalDateTime:
        return LocalDateTime.from_iso_int(value)
    elif expected_type == LocalDate:
        return LocalDate.from_iso_int(value)
    elif expected_type == LocalTime:
        return LocalTime.from_iso_int(value)
    elif expected_type == int:
        return value
    elif expected_type == float:
        return value
    elif expected_type == ObjectId:
        return value
    else:
        raise Exception(f'Cannot deduce type {expected_type}')
