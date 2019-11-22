import attr
import numpy as np
from bson import ObjectId
from enum import IntEnum
from typing import Dict, Any, get_type_hints, TypeVar, Union, List
from typing_inspect import get_origin, get_args

from datacentric.types.string_util import StringUtil
from datacentric.storage.class_info import ClassInfo
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.key import Key
from datacentric.storage.record import Record
from datacentric.storage.data import Data

TRecord = TypeVar('TRecord', bound=Record)


# Serialization: object -> dict

def serialize(obj: TRecord):
    dict_ = _serialize_class(obj)
    dict_['_t'] = obj.__class__.__name__
    dict_['_dataset'] = obj.data_set
    dict_['_key'] = obj.key
    dict_['_id'] = obj.id_

    return dict_


def _serialize_class(obj: TRecord):
    dict_ = dict()

    cls_type = type(obj)
    class_name = cls_type.__name__
    dict_['_t'] = class_name

    mro = cls_type.__mro__
    fields = attr.fields(cls_type)
    if Record in mro:
        serializable_fields = fields[4:]
    elif Data in mro:
        serializable_fields = fields
    else:
        raise Exception(f'Cannot serialize class {class_name} not derived from Record or Data.')

    field: attr.Attribute
    for field in serializable_fields:
        value = getattr(obj, field.name)
        value_type = type(value)
        is_optional = field.metadata.get('optional', False)
        if value is None:
            if not is_optional:
                raise Exception(f'Missing required field: {field.name} in type: {class_name}')
            continue

        if issubclass(value_type, Key):
            serialized_value = value.value
        elif issubclass(value_type, Data):
            serialized_value = _serialize_class(value)
        elif issubclass(value_type, IntEnum):
            serialized_value = value.name
        elif value_type is list:
            serialized_value = _serialize_list(value, is_optional)
        else:
            serialized_value = _serialize_primitive(value)

        dict_[StringUtil.to_pascal_case(field.name)] = serialized_value
    return dict_


def _serialize_list(list_, is_optional: bool) -> List[Any]:
    result: List[Any] = []
    for value in list_:
        if value is None:
            if is_optional:
                result.append(None)
            else:
                raise Exception('Lists not marked as optional cannot contain None elements.')
        else:
            value_type = type(value)
            if issubclass(value_type, Key):
                result.append(value.value)
            elif issubclass(value_type, Data):
                result.append(_serialize_class(value))
            elif issubclass(value_type, IntEnum):
                result.append(value.name)
            elif value_type is list:
                raise Exception(f'List of lists are prohibited.')
            else:
                result.append(_serialize_primitive(value))
    return result


def _serialize_primitive(value):
    value_type = type(value)
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
    # TODO: check for pymongo.binary.Binary to speed-up
    elif value_type == np.ndarray:
        return value.tolist()
    else:
        raise Exception(f'Cannot serialize type {value_type.__name__}')


# Deserialization: dict -> object


def deserialize(dict_: Dict) -> TRecord:
    data_set = dict_.pop('_dataset')
    _key = dict_.pop('_key')
    id_ = dict_.pop('_id')

    new_obj: TRecord = _deserialize_class(dict_)

    new_obj.__setattr__('data_set', data_set)
    new_obj.__setattr__('_key', _key)
    new_obj.__setattr__('id_', id_)

    return new_obj


def _deserialize_class(dict_: Dict[str, Any]) -> TRecord:
    type_name: str = dict_.pop('_t')

    type_info = ClassInfo.get_type(type_name)
    new_obj = type_info()

    for dict_key, dict_value in dict_.items():
        slot = StringUtil.to_snake_case(dict_key)
        hints = get_type_hints(type_info)
        member_type = hints[slot]

        # Resolve Optional[Type] case
        if get_origin(member_type) is not None and get_origin(member_type) is Union:
            union_args = get_args(member_type)
            if union_args[1] is type(None):
                member_type = union_args[0]

        if get_origin(member_type) is not None and get_origin(member_type) is list:
            deserialized_value = _deserialize_list(member_type, dict_value)
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
        raise TypeError(f'Cannot deduce type {expected_type}')
