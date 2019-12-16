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

from enum import IntEnum


class IsoDayOfWeek(IntEnum):
    """
    Equates the days of the week with their numerical value according to
    ISO-8601.
    """

    Empty = 0,
    """
    Value indicating no day of the week; this will never be returned
    by any IsoDayOfWeek property, and is not valid as an argument to
    any method.
    """

    Monday = 1,
    """Value representing Monday (1)."""

    Tuesday = 2,
    """Value representing Tuesday (2)."""

    Wednesday = 3,
    """Value representing Wednesday (3)."""

    Thursday = 4,
    """Value representing Thursday (4)."""

    Friday = 5,
    """Value representing Friday (5)."""

    Saturday = 6,
    """Value representing Saturday (6)."""

    Sunday = 7,
    """Value representing Sunday (7)."""
