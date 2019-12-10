import attr
import importlib
import inspect
import pkgutil

from abc import ABC
from enum import IntEnum
from typing import List, Any, Deque, Set, TypeVar, Type, Optional, Union
from typing_inspect import get_origin, get_args

from datacentric import TemporalMongoDataSource, EnvType
from datacentric.primitive.string_util import StringUtil
from datacentric.schema.declaration.element_decl import ElementDecl
from datacentric.schema.declaration.module import Module
from datacentric.schema.declaration.type_kind import TypeKind
from datacentric.schema.declaration.yes_no import YesNo
from datacentric.storage.context import Context
from datacentric.storage.data import Data
from datacentric.storage.record import Record
from datacentric.storage.root_record import RootRecord
from datacentric.schema.declaration.type_decl import TypeDecl
from datacentric.schema.declaration.enum_decl import EnumDecl

T = TypeVar('T')
TData = TypeVar('TData', bound=Data)
TEnum = TypeVar('TEnum', bound=IntEnum)


def get_derived_types(module_name: str, base_type: Type[T]) -> Set[Type[T]]:
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

    derived_types.remove(base_type)
    return derived_types


def _process_module_name(module_name: str):
    package_name = module_name.split('.')[0]
    if package_name == 'datacentric':
        package_name = 'data_centric'

    return StringUtil.to_pascal_case(package_name)


def _create_type_decl_key(module: str, name: str) -> str:
    module_name = _process_module_name(module)
    return TypeDecl.create_key(module=Module.create_key(module_name=module_name), name=name)


def _get_kind(type_: Type[TData]) -> Optional[TypeKind]:
    if ABC in type_.__bases__:
        return TypeKind.Abstract
    elif Record not in type_.mro():
        return TypeKind.Element
    else:
        return None


def _get_inherit(type_: Type[TData]) -> Optional[str]:
    base = [x for x in type_.__bases__ if x is not ABC][0]
    base_types = [Data, Record, RootRecord]
    if base not in base_types:
        return _create_type_decl_key(base.__module__, base.__name__)
    return None


def _process_elements(type_: Type[TData]) -> List[ElementDecl]:
    attributes = attr.fields(type_)
    non_private_fields = [x for x in attributes if not x.name.startswith('_') and x.init]

    result: List[ElementDecl] = []
    for field in non_private_fields:  # type: attr.Attribute
        element = ElementDecl()
        type_hint = field.type
        is_list = get_origin(type_hint) is not None and get_origin(type_hint) is list

        if is_list:
            element.vector = YesNo.Y
        element.name = StringUtil.to_pascal_case(field.name)
        element.label = StringUtil.to_pascal_case(field.name)

        # TODO: get comment
        # element.comment

        element.optional = YesNo.Y if field.metadata.get('optional', False) else None

        # TODO:
        element.category = 'Data' if element.vector == YesNo.Y else None

        result.append(element)
    return result


def to_type_declaration(type_: Type[TData]) -> TypeDecl:
    result = TypeDecl()

    result.module = Module.create_key(module_name=_process_module_name(type_.__module__))
    result.category = StringUtil.to_pascal_case(type_.__module__)
    result.name = type_.__name__
    result.label = type_.__name__
    result.comment = type_.__doc__
    result.kind = _get_kind(type_)
    result.inherit = _get_inherit(type_)

    # TODO: complete after redesign
    # result.index

    # TODO: complete after hints for handler functions
    # result.declare
    # result.implement

    result.elements = _process_elements(type_)

    return result


def to_enum_declaration(type_: Type[TEnum]) -> EnumDecl:
    pass


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

    type_declarations = [to_type_declaration(x) for x in get_derived_types('datacentric', Data)]
    context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
