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
    from datacentric.log.log import Log
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

    __slots__ = ('__log', '__data_source', '__data_set')

    __log: Optional['Log']
    __data_source: Optional['DataSource']
    __data_set: Optional[ObjectId]

    def __init__(self):
        """
        Set instant variables to None here. They will be
        set and then initialized by the respective
        property setter.
        """

        self.__log = None
        """Logging interface of the context."""

        self.__data_source = None
        """Default data source of the context."""

        self.__data_set = None
        """Default dataset of the context."""

    def __enter__(self):
        """
        Supports with syntax for resource disposal.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Supports with syntax for resource disposal.
        """

        # Dispose method releases resources such as file handles
        self.dispose()

        # Return False to propagate exception to the caller
        return False

    # --- PROPERTIES

    @property
    def log(self) -> 'Log':
        """Return log property, error message if not set."""

        # Define log here to avoid a cyclic reference
        from datacentric.log.log import Log

        if not self.__log:
            raise Exception('Log property is not set in Context.')
        return self.__log

    @log.setter
    def log(self, value: 'Log'):
        """Set log property and pass self to its init method."""
        self.__log = value
        self.__log.init(self)

    @property
    def data_source(self) -> 'DataSource':
        """Return data_source property, error message if not set."""

        # Define data source here to avoid a cyclic reference
        from datacentric.storage.data_source import DataSource

        if not self.__data_source:
            raise Exception('Data source property is not set in Context.')
        return self.__data_source

    @data_source.setter
    def data_source(self, value: 'DataSource'):
        """Set data_source property and pass self to its init method."""
        self.__data_source = value
        self.__data_source.init(self)

    @property
    def data_set(self) -> ObjectId:
        """Return data_set property, error message if not set."""

        if not self.__data_set:
            raise Exception('Dataset property is not set in Context.')
        return self.__data_set

    @data_set.setter
    def data_set(self, value: ObjectId):
        """Set data_set property."""
        self.__data_set = value

    # --- METHODS

    def dispose(self) -> None:
        """
        Releases resources and calls base.dispose().

        IMPORTANT - Every override of this method must call base.dispose()
        after executing its own code.
        """
        # TODO - implement
        pass


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
