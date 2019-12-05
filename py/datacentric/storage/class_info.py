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

from typing import Dict, List
import typing_inspect


class ClassInfo:
    """Contains reflection based helper static methods.
    """
    __is_initialized: bool = False
    __data_types_map: Dict[str, type] = dict()

    @staticmethod
    def get_type(name: str) -> type:
        """Returns data derived type given its name."""
        if not ClassInfo.__is_initialized:
            from datacentric.storage.data import Data
            children = ClassInfo.__get_runtime_imported_data(Data, [])
            for child in children:
                if child not in ClassInfo.__data_types_map:
                    ClassInfo.__data_types_map[child.__name__] = child
            ClassInfo.__is_initialized = True

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
        from datacentric.storage.data import Data
        from datacentric.storage.record import Record
        from datacentric.storage.root_record import RootRecord
        root_types = [Data, Record, RootRecord]

        if type_.mro()[0] in root_types:
            raise Exception(f'Cannot get root type from root type.')
        type_mro = type_.mro()
        for root_type in root_types:
            if root_type in type_mro:
                index = type_mro.index(root_type)
                return type_mro[index - 1]
        raise Exception(f'Type is not derived from Data, Record, or RootRecord.')

    @staticmethod
    def __get_runtime_imported_data(type_: type, children: List[type]) -> List[type]:
        """For the given type recursively adds its children."""
        current_children = type_.__subclasses__()
        for t in current_children:
            ClassInfo.__get_runtime_imported_data(t, children)
        children.extend(current_children)
        return children
