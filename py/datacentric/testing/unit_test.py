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
from datacentric.storage.context import Context
from datacentric.storage.unit_test_context import UnitTestContext
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord
from datacentric.testing.unit_test_complexity import UnitTestComplexity


@attr.s(slots=True, auto_attribs=True)
class UnitTest(TypedRecord):
    """
    Base class for executing the tests using:

    * A standard xUnit test runner; or
    * A handler via CLI or the front end

    This makes it possible to test not only inside the development
    environment but also on a deployed version of the application where
    access to the xUnit test runner is not available.
    """
    _keys = ('unit_test_name',)

    unit_test_name: str = attr.ib(default=None, kw_only=True)
    """
    Unique unit test name.

    The name is set to the fully qualified test class name
    in the constructor of this class.
    """

    complexity: UnitTestComplexity = attr.ib(default=None, kw_only=True)
    """
    Test complexity level.

    Higher complexity results in more comprehensive testing at
    the expect of longer test running times.
    """

    # --- METHODS

    def create_method_context(self):
        """"
        Create a new context for the test method. The way the context
        is created depends on how the test is invoked.

        When invoked inside xUnit test runner, Context will be null
        and a new copy of unit test runner will be created.

        When invoked inside DataCentric, Init(context) will be called
        before this method and will set Context. This method will then
        create a new dataset inside this Context for each test method.

        This method may be used by the unit tests in this class or as
        part of the test data set up by other classes.
        """

        if not self.context:
            # If Context is null, the class is invoked via xUnit
            # runner and we should create a unit test context
            result: Context = UnitTestContext()
            return result
        else:
            # If Context is not null, this means Init(context) method was previously
            # called by DataCentric. We will then create a new dataset for each
            # unit test method
            raise NotImplementedError()

    def run_all(self):
        """
        Run all methods in this class that have [Fact] or [Theory] attribute.

        This method will run each of the test methods using its own instance
        of the test class in parallel.
        """
        raise NotImplementedError()


@attr.s(slots=True, auto_attribs=True)
class UnitTestKey(TypedKey[UnitTest]):
    pass
