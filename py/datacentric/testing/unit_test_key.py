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
from typing import Union, Optional, List, Any
from abc import ABC, abstractmethod
from datacentric.storage.key import Key


class UnitTestKey(Key):
    """
    Base class for executing the tests using:

    * A standard xUnit test runner; or
    * A handler via CLI or the front end

    This makes it possible to test not only inside the development
    environment but also on a deployed version of the application where
    access to the xUnit test runner is not available.
    """
    pass
