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


class Key(ABC):
    """
    Base class of a foreign key.

    The sole purpose of foreign key classes derived from this class
    is to provide type safety by servinv as annotations (hints).

    To prevent this abstract base class from being instantiated, it
    includes an guard method that should not be implemented.
    """

    @abstractmethod
    def abstract_class_guard(self) -> None:
        """
        Guard method to prevent this abstract base class from
        being instantiated.
        """
        pass
