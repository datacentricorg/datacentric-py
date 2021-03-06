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
import importlib
import inspect
import pkgutil
import datetime as dt

from abc import ABC
from enum import IntEnum
from typing import List, Set, TypeVar, Type, Optional, Any, Dict

from bson import ObjectId
from typing_inspect import get_origin, get_args

from datacentric.primitive.string_util import StringUtil
from datacentric.schema.declaration.element_decl import ElementDecl
from datacentric.schema.declaration.enum_item import EnumItem
from datacentric.schema.declaration.module import Module
from datacentric.schema.declaration.type_kind import TypeKind
from datacentric.schema.declaration.value_decl import ValueDecl
from datacentric.schema.declaration.value_param_type import ValueParamType
from datacentric.schema.declaration.yes_no import YesNo
from datacentric.schema.declaration.type_decl import TypeDecl
from datacentric.schema.declaration.enum_decl import EnumDecl
from datacentric.storage.context import Context
from datacentric.storage.data import Data
from datacentric.storage.record import Record
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.storage.env_type import EnvType
from datacentric.storage.class_info import ClassInfo
from datacentric.storage.versioning_method import VersioningMethod

T = TypeVar('T')
TData = TypeVar('TData', bound=Data)
TEnum = TypeVar('TEnum', bound=IntEnum)


def _format_comment(comment: Optional[str]) -> Optional[str]:
    """Fixes comment indentation."""
    if comment is None:
        return None
    lines = [x.strip(' ') for x in comment.split('\n')]
    return '\n'.join(lines)


def _category_from_module(module_: str) -> str:
    """Process full module of type to declaration category."""
    if module_.startswith('datacentric'):
        module_ = 'data_centric' + module_[len('datacentric'):]
    return StringUtil.to_pascal_case(module_)


def _module_from_module_name(module_name: str) -> str:
    """Process full module of type to declaration module."""
    package_name = module_name.split('.')[0]
    if package_name == 'datacentric':
        package_name = 'data_centric'

    return StringUtil.to_pascal_case(package_name)


def _create_type_declaration_key(module: str, name: str) -> str:
    """Create proper type delcaration key."""
    module_name = _module_from_module_name(module)
    return TypeDecl.create_key(module=Module.create_key(module_name=module_name), name=name)


def _create_enum_declaration_key(module: str, name: str) -> str:
    """Create proper enum delcaration key."""
    module_name = _module_from_module_name(module)
    return EnumDecl.create_key(module=Module.create_key(module_name=module_name), name=name)


def _get_kind(type_: Type[TData]) -> Optional[TypeKind]:
    """Extract kind information from type."""
    if ABC in type_.__bases__:
        return TypeKind.Abstract
    elif Record not in type_.mro():
        return TypeKind.Element
    else:
        return None


def _get_inherit(type_: Type[TData]) -> Optional[str]:
    """Process base class and convert it to reference
    to base type in declaration format.
    """
    base = [x for x in type_.__bases__ if x is not ABC][0]
    base_types = [Data, Record]
    if base not in base_types:
        return _create_type_declaration_key(base.__module__, base.__name__)
    return None


def _to_type_member(type_: type, metadata_: Dict[Any, Any]) -> ElementDecl:
    """Resolve attribute type hint to type related part of element declaration."""
    result = ElementDecl()

    # Get argument of List[...] type hint
    is_list = get_origin(type_) is not None and get_origin(type_) is list
    if is_list:
        type_ = get_args(type_)[0]

    key_ = metadata_.get('key', None)
    if key_ is not None and type_ is str:
        key_type = ClassInfo.get_type(key_)
        result.key = _create_type_declaration_key(key_type.__module__, key_)
        return result

    meta_type = metadata_.get('type', None)

    # Primitive types
    if type_ is str:
        result.value = ValueDecl(type=ValueParamType.String)
    elif type_ is bool:
        result.value = ValueDecl(type=ValueParamType.NullableBool)
    elif type_ is float:
        result.value = ValueDecl(type=ValueParamType.NullableDouble)
    elif type_ is ObjectId:
        result.value = ValueDecl(type=ValueParamType.NullableTemporalId)

    # Date additional cases
    elif type_ is dt.date:
        result.value = result.value = ValueDecl(type=ValueParamType.NullableDate)
    elif type_ is dt.time:
        result.value = result.value = ValueDecl(type=ValueParamType.NullableTime)
    # dt.datetime depends on metadata
    elif type_ is dt.datetime:
        if meta_type == 'Instant':
            result.value = ValueDecl(type=ValueParamType.NullableInstant)
        elif meta_type is None:
            result.value = ValueDecl(type=ValueParamType.NullableDateTime)
        else:
            raise Exception(f'Unexpected dt.datetime and metadata type combination: dt.datetime + {type_.__name__}')

    # Restore int/long/Local... separation using info from metadata
    elif type_ is int:
        if meta_type == 'long':
            result.value = ValueDecl(type=ValueParamType.NullableLong)
        elif meta_type == 'LocalDate':
            result.value = ValueDecl(type=ValueParamType.NullableDate)
        elif meta_type == 'LocalTime':
            result.value = ValueDecl(type=ValueParamType.NullableTime)
        elif meta_type == 'LocalMinute':
            result.value = ValueDecl(type=ValueParamType.NullableMinute)
        elif meta_type == 'LocalDateTime':
            result.value = ValueDecl(type=ValueParamType.NullableDateTime)
        elif meta_type is None:
            result.value = ValueDecl(type=ValueParamType.NullableInt)
        else:
            raise Exception(f'Unexpected int and metadata type combination: int + {type_.__name__}')

    elif issubclass(type_, Data):
        result.data = _create_type_declaration_key(type_.__module__, type_.__name__)
    elif issubclass(type_, IntEnum):
        result.enum = _create_enum_declaration_key(str(type_.__module__), type_.__name__)
    else:
        raise Exception(f'Unexpected type {type_.__name__}')
    return result


def _process_elements(type_: Type[TData]) -> Optional[List[ElementDecl]]:
    """Extract element declarations from attributes."""
    all_attributes = attr.fields(type_)
    own_attributes = [x for x in all_attributes if x.name in type_.__slots__]

    own_public_attrs = [x for x in own_attributes if not x.name.startswith('_') and x.init]

    if len(own_attributes) == 0:
        return None

    result: List[ElementDecl] = []
    for field in own_public_attrs:  # type: attr.Attribute
        element = _to_type_member(field.type, field.metadata)

        is_list = get_origin(field.type) is not None and get_origin(field.type) is list

        element.vector = YesNo.Y if is_list else None
        element.name = StringUtil.to_pascal_case(field.name)
        element.label = StringUtil.to_pascal_case(field.name)
        element.comment = _format_comment(field.__doc__)
        element.optional = YesNo.Y if field.metadata.get('optional', False) else None
        # TODO:
        element.category = 'Data' if element.vector == YesNo.Y else None

        result.append(element)
    return result


def to_type_declaration(type_: Type[TData]) -> TypeDecl:
    """Parse type information to type declaration."""
    result = TypeDecl()

    result.module = Module.create_key(module_name=_module_from_module_name(type_.__module__))
    result.category = _category_from_module(type_.__module__)
    result.name = type_.__name__
    result.label = type_.__name__
    result.comment = _format_comment(type_.__doc__)
    result.kind = _get_kind(type_)
    result.inherit = _get_inherit(type_)

    # TODO: complete after redesign
    # result.index

    # TODO: complete after hints for handler functions
    # result.declare
    # result.implement

    result.elements = _process_elements(type_)

    # Extract keys from create_key signature
    if 'create_key' in vars(type_):
        create_key_func = getattr(type_, 'create_key')
        if callable(create_key_func):
            func_params = inspect.signature(create_key_func).parameters
            key_names = [StringUtil.to_pascal_case(x) for x in func_params.keys()]
            if key_names:
                result.keys = key_names

    return result


def to_enum_declaration(enum_: Type[TEnum]) -> EnumDecl:
    """Parse type information to enum declaration."""
    result = EnumDecl()
    result.name = enum_.__name__
    result.comment = _format_comment(str(enum_.__doc__))
    result.category = _category_from_module(str(enum_.__module__))
    result.module = Module.create_key(module_name=_module_from_module_name(str(enum_.__module__)))
    result.label = enum_.__name__

    # Process enum items
    result.items = []
    for item in enum_:
        enum_item = EnumItem(name=item.name, label=item.name, comment=_format_comment(item.__doc__))
        result.items.append(enum_item)

    return result


if __name__ == '__main__':
    data_source = TemporalMongoDataSource()
    data_source.env_type = EnvType.Test
    data_source.env_group = 'Schema'
    data_source.env_name = 'Default'
    data_source.versioning_method = VersioningMethod.Temporal

    context = Context()
    context.data_source = data_source

    # Delete (drop) the database to clear the existing data
    context.data_source.delete_db()

    # Create Common dataset and assign it to data_set property of this context
    context.data_set = context.data_source.create_data_set('Common')

    # Convert extracted types to declarations
    type_declarations = [to_type_declaration(x) for x in ClassInfo.get_derived_types('datacentric', Data)]
    enum_declarations = [to_enum_declaration(x) for x in ClassInfo.get_derived_types('datacentric', IntEnum)]

    # Save declarations to db
    context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
    context.data_source.save_many(EnumDecl, enum_declarations, context.data_set)
