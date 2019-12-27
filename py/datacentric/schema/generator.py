import attr
import importlib
import inspect
import pkgutil
import datetime as dt

from abc import ABC
from enum import IntEnum
from typing import List, Set, TypeVar, Type, Optional, Union, Any, Dict

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
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.date_time.instant import Instant
from datacentric.storage.context import Context
from datacentric.storage.data import Data
from datacentric.storage.record import Record
from datacentric.storage.root_record import RootRecord
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.storage.env_type import EnvType

T = TypeVar('T')
TData = TypeVar('TData', bound=Data)
TEnum = TypeVar('TEnum', bound=IntEnum)


def get_derived_types(module_name: str, base_type: Type[T]) -> Set[Type[T]]:
    """Extract all derived classes from specified module."""
    try:
        module_ = __import__(module_name)
    except ImportError as error:
        raise Exception(f'Cannot import module: {error.name}. Check sys.path')

    derived_types: Set[Type[T]] = set()

    packages = list(pkgutil.walk_packages(path=module_.__path__, prefix=module_.__name__ + '.'))
    modules = [x for x in packages if not x.ispkg]
    for m in modules:
        try:
            m_imp = importlib.import_module(m.name)
        except SyntaxError as error:
            print(f'Cannot import module: {m.name}. Error: {error.msg}. Line: {error.lineno}, {error.offset}')
            continue
        except NameError as error:
            print(f'Cannot import module: {m.name}. Error: {error.args}')
            continue
        classes = inspect.getmembers(m_imp, inspect.isclass)
        derived_types.update([x[1] for x in classes if issubclass(x[1], base_type)])

    if base_type in derived_types:
        derived_types.remove(base_type)
    return derived_types


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
    base_types = [Data, Record, RootRecord]
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

    is_union = get_origin(type_) is not None and get_origin(type_) is Union

    # Date classes and keys are represented with Union
    if is_union:
        union_args = get_args(type_)
        if len(union_args) != 2:
            raise Exception(f'Expected two args in Union, got {len(union_args)}')
        first_arg, second_arg = union_args
        if first_arg is str and issubclass(second_arg, Key):
            if not second_arg.__name__.endswith('Key'):
                raise Exception(f'Expected ...Key, got {second_arg.__name__}')
            result.key = _create_type_declaration_key(second_arg.__module__, second_arg.__name__[:-3])
        if first_arg is int:
            if second_arg is LocalDate:
                result.value = ValueDecl(type=ValueParamType.NullableDate)
            elif second_arg is LocalTime:
                result.value = ValueDecl(type=ValueParamType.NullableTime)
            elif second_arg is LocalDateTime:
                result.value = ValueDecl(type=ValueParamType.NullableDateTime)
            elif second_arg is LocalMinute:
                result.value = ValueDecl(type=ValueParamType.NullableMinute)
            else:
                raise Exception(f'Unexpected Union args combination.')
        if first_arg is dt.datetime and second_arg == Instant:
            result.value = ValueDecl(type=ValueParamType.NullableInstant)

    # Primitive types
    elif type_ is str:
        result.value = ValueDecl(type=ValueParamType.String)
    elif type_ is bool:
        result.value = ValueDecl(type=ValueParamType.NullableBool)
    elif type_ is float:
        result.value = ValueDecl(type=ValueParamType.NullableDouble)
    elif type_ is ObjectId:
        result.value = ValueDecl(type=ValueParamType.NullableTemporalId)

    # Restore int/long separation using info from metadata
    elif type_ is int:
        if metadata_.get('type', None) == 'long':
            result.value = ValueDecl(type=ValueParamType.NullableLong)
        else:
            result.value = ValueDecl(type=ValueParamType.NullableInt)

    elif issubclass(type_, Data):
        result.data = _create_type_declaration_key(type_.__module__, type_.__name__)
    elif issubclass(type_, IntEnum):
        result.enum = _create_type_declaration_key(str(type_.__module__), type_.__name__)
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
    context = Context()
    context.data_source = TemporalMongoDataSource(
        env_type=EnvType.Test,
        env_group='Schema',
        env_name='Default'
    )

    # Delete (drop) the database to clear the existing data
    context.data_source.delete_db()

    # Create Common dataset and assign it to data_set property of this context
    context.data_set = context.data_source.create_common()

    # Convert extracted types to declarations
    type_declarations = [to_type_declaration(x) for x in get_derived_types('datacentric', Data)]
    enum_declarations = [to_enum_declaration(x) for x in get_derived_types('datacentric', IntEnum)]

    # Save declarations to db
    context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
    context.data_source.save_many(EnumDecl, enum_declarations, context.data_set)
