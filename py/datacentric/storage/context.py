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

from typing import Optional
import inspect
from bson.objectid import ObjectId

# To prevent linter error on type hint in quotes
if False:
    from datacentric.logging.log import Log
    from datacentric.storage.data_source import DataSource


class Context:
    """
    Context provides:

    * Default data source
    * Default dataset of the default data source
    * Logging
    * Progress reporting
    * Filesystem access (if available)
    """

    __log: Optional['Log']
    data_source: Optional['DataSource']
    data_set: Optional[ObjectId]

    def __init__(self):

        self.__log = None
        """Logging interface."""

        self.data_source = None
        """Default data source of the context."""

        self.data_set = None
        """Default dataset of the context."""

    # --- PROPERTIES

    @property
    def log(self) -> 'Log':
        """Logging interface."""

        # Define log
        from datacentric.logging.log import Log

        if not self.__log:
            raise Exception('fLog property is not set in {GetType().Name}.')
        return self.__log

    @log.setter
    def log(self, value: 'Log'):
        """Logging interface."""
        self.__log = value
        self.__log.init(self)

    # --- METHODS

    def configure(self, module) -> None:
        """
        Invokes static method configure(context) method with self as argument
        for every class that is loaded by the argument and marked with
        ConfigurableAttribue class attribute.

        The method configure(context) may be used to configure:

        * Reference data, and
        * In case of test mocks, test data

        The order in which configure(context) method is invoked when
        multiple classes marked by ConfigurableAttribue are present
        is undefined. The implementation of configure(context) should
        not rely on any existing data, and should not invoke other
        Configure(context) method of other classes.

        The attribute ConfigurableAttribue is not inherited. To invoke
        Configure(context) method for multiple classes within the same
        inheritance chain, specify ConfigurableAttribue for each
        class that provides configure(context) method.
        """

        for name, obj in inspect.getmembers(module, lambda x: inspect.isclass(x)):
            print(name)
            print(inspect.getmembers(obj))
