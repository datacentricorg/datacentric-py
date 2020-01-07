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

import gc
import importlib
import inspect
import pkgutil
from typing import Dict, List, Type, Set, TypeVar

T = TypeVar('T')


class ClassInfo:
    """
    Contains reflection based helper static methods.
    """
    __is_initialized: bool = False
    __data_types_map: Dict[str, type] = dict()

    @staticmethod
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

    @staticmethod
    def get_type(name: str) -> type:
        """Returns data derived type given its name."""

        if not ClassInfo.__is_initialized:
            from datacentric.storage.data import Data
            # Resolves issue with classes duplicates in __subclasses__()
            gc.collect()
            children = ClassInfo.__get_runtime_imported_data(Data, [])
            for child in children:
                if child.__name__ not in ClassInfo.__data_types_map:
                    ClassInfo.__data_types_map[child.__name__] = child
            ClassInfo.__is_initialized = True

        if name not in ClassInfo.__data_types_map:
            # Try to update map one more time. This scenario is possible depending on
            # first call to get_type and which classes where imported at that moment.
            from datacentric.storage.data import Data
            # Resolves issue with classes duplicates in __subclasses__()
            gc.collect()
            children = ClassInfo.__get_runtime_imported_data(Data, [])
            for child in children:
                if child.__name__ not in ClassInfo.__data_types_map:
                    ClassInfo.__data_types_map[child.__name__] = child

            if name not in ClassInfo.__data_types_map:
                raise Exception(f'Class {name} is not found in ClassInfo data types map')

        return ClassInfo.__data_types_map[name]

    @staticmethod
    def get_ultimate_base(type_: type) -> type:
        """
        Returns the ultimate base class of the inheritance chain which
        determines the collection name.

        This is the class derived directly from Data, Record, or RootRecord.
        """

        # TODO - cache ClassInfo in singleton dict so it is not recomputed every time

        from datacentric.storage.data import Data
        from datacentric.storage.record import Record
        from datacentric.storage.root_record import RootRecord

        root_types = [Data, Record, RootRecord]

        type_mro = type_.mro()
        if type_mro[0] in root_types:
            raise Exception('Ultimate base is undefined for Data, Record, RootRecord, '
                            'only for classes derived from them.')

        for i in range(1, len(type_mro)):
            if type_mro[i] in root_types:
                return type_mro[i - 1]
        raise Exception(f'Type is not derived from Data, Record, or RootRecord.')

    @staticmethod
    def get_inheritance_chain(type_: type) -> List[str]:
        """
        Returns the inheritance chain of the class as a list of
        class name strings, starting from RootRecord or Record or Data
        and ending with the class itself.

        The class must be derived from Data, error message otherwise.
        """

        # TODO - cache ClassInfo in singleton dict so it is not recomputed every time

        from datacentric.storage.data import Data
        from datacentric.storage.record import Record
        from datacentric.storage.root_record import RootRecord

        type_mro = type_.mro()
        if type_mro[0] is Record:
            raise Exception(f'Cannot get inheritance chain for the Record class, '
                            f'only for classes derived from it.')

        if RootRecord in type_mro:
            idx = type_mro.index(RootRecord)
            return [x.__name__ for x in type_mro[idx::-1]]
        elif Record in type_mro:
            idx = type_mro.index(Record)
            return [x.__name__ for x in type_mro[idx::-1]]
        elif Data in type_mro:
            idx = type_mro.index(Data)
            return [x.__name__ for x in type_mro[idx::-1]]
        raise Exception(f'Type is not derived from Data')

    @staticmethod
    def __get_runtime_imported_data(type_: type, children: List[type]) -> List[type]:
        """For the given type recursively adds its children."""
        current_children = type_.__subclasses__()
        for t in current_children:
            ClassInfo.__get_runtime_imported_data(t, children)
        children.extend(current_children)
        return children
