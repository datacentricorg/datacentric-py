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

from abc import ABC, abstractmethod
from typing import Optional
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord
from datacentric.testing.test_complexity import TestComplexity


class UnitTestKey(TypedKey['UnitTest']):
    """
    Base class for executing the tests using:

    * A standard xUnit test runner; or
    * A handler via CLI or the front end

    This makes it possible to test not only inside the development
    environment but also on a deployed version of the application where
    access to the xUnit test runner is not available.
    """

    __slots__ = ('unit_test_name',)

    unit_test_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.unit_test_name = None
        """
        Unique test name.

        The name is set to the fully qualified test class name
        in the constructor of this class.
        """


class UnitTest(TypedRecord[UnitTestKey]):
    """
    Base class for executing the tests using:

    * A standard xUnit test runner; or
    * A handler via CLI or the front end

    This makes it possible to test not only inside the development
    environment but also on a deployed version of the application where
    access to the xUnit test runner is not available.
    """

    __slots__ = ('unit_test_name', 'complexity')

    unit_test_name: Optional[str]
    complexity: Optional[TestComplexity]

    def __init__(self):
        super().__init__()

        self.unit_test_name = None
        """
        Unique test name.

        The name is set to the fully qualified test class name
        in the constructor of this class.
        """

        self.complexity = None
        """
        Test complexity level.

        Higher complexity results in more comprehensive testing at
        the expect of longer test running times.
        """

    def run_all(self):
        """
        Run all methods in this class that have [Fact] or [Theory] attribute.

        This method will run each of the test methods using its own instance
        of the test class in parallel.
        """
        raise NotImplementedError()
