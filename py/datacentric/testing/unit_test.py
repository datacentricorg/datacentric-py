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
from typing import Union
from datacentric.storage.context import Context
from datacentric.storage.record import Record
from datacentric.storage.unit_test_context import UnitTestContext
from datacentric.testing.unit_test_key import UnitTestKey
from datacentric.testing.unit_test_complexity import UnitTestComplexity


@attr.s(slots=True, auto_attribs=True)
class UnitTest(Record):
    """
    Base class for executing the tests using:

    * A standard xUnit test runner; or
    * A handler via CLI or the front end

    This makes it possible to test not only inside the development
    environment but also on a deployed version of the application where
    access to the xUnit test runner is not available.
    """

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

    def to_key(self) -> str:
        """Get UnitTest key."""
        return 'UnitTest=' + self.unit_test_name

    @classmethod
    def create_key(cls, *, unit_test_name: str) -> Union[str, UnitTestKey]:
        """Create UnitTest key."""
        return 'UnitTest=' + unit_test_name

    # @abstractmethod
    def run_all(self):
        """
        Run all methods in this class that have [Fact] or [Theory] attribute.

        This method will run each of the test methods using its own instance
        of the test class in parallel.
        """
        raise NotImplementedError
