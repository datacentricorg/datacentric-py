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


class ValueParamType(IntEnum):
    """Primitive type of a handler parameter or type element."""

    Empty = 0,
    """
    Indicates that enum value is not set.

    In programming languages where enum defaults to the first item when
    not set, making Empty the first item prevents unintended assignment
    of a meaningful value.
    """

    Bool = 1,
    """Bool value."""

    NullableBool = 2,
    """Nullable bool value."""

    Int = 3,
    """Int value."""

    NullableInt = 4,
    """Nullable int value."""

    Long = 5,
    """Long value."""

    NullableLong = 6,
    """Nullable long value."""

    Double = 7,
    """Double value."""

    NullableDouble = 8,
    """Nullable double value."""

    Date = 9,
    """Date value."""

    NullableDate = 10,
    """Nullable date value."""

    DateTime = 11,
    """DateTime value."""

    NullableDateTime = 12,
    """Nullable DateTime value."""

    String = 13,
    """String value."""

    Binary = 14,
    """Binary value."""

    Key = 15,
    """Key value."""

    Data = 16,
    """Generic data value."""

    Variant = 17,
    """Variant value."""

    Decimal = 18,
    """Decimal value."""

    NullableDecimal = 19,
    """Nullable decimal value."""

    Time = 20,
    """Time value."""

    NullableTime = 21,
    """Nullable time value."""

    TemporalId = 22,
    """TemporalId."""

    NullableTemporalId = 23,
    """Nullable TemporalId."""

    Minute = 24,
    """Minute."""

    NullableMinute = 25,
    """Nullable minute."""

    Instant = 26,
    """Instant."""

    NullableInstant = 27,
    """Nullable instant."""
