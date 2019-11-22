import attr
from enum import IntEnum
from typing import List

from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.data import Data


@attr.s(slots=True, auto_attribs=True)
class ElementSample(Data):
    double_element3: float = attr.ib(default=None, kw_only=True)
    string_element3: str = attr.ib(default=None, kw_only=True)


class SampleEnum(IntEnum):
    Empty = 0
    EnumValue1 = 1
    EnumValue2 = 2


@attr.s(slots=True, auto_attribs=True)
class BaseSample(TypedRecord['BaseSampleKey']):
    record_id: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    double_element: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_element: LocalDate = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_time_element: LocalTime = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_minute_element: LocalMinute = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    local_date_time_element: LocalDateTime = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    enum_value: SampleEnum = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    version: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})


@attr.s(slots=True, auto_attribs=True)
class BaseSampleKey(TypedKey[BaseSample]):
    record_id: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    record_index: int = attr.ib(default=None, kw_only=True, metadata={'optional': True})


@attr.s(slots=True, auto_attribs=True)
class DerivedSample(BaseSample):
    double_element2: float = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    string_element2: str = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_string: List[str] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    list_of_nullable_double: List[float] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    data_element: ElementSample = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    data_element_list: List[ElementSample] = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    key_element: BaseSampleKey = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    key_element_list: List[BaseSampleKey] = attr.ib(default=None, kw_only=True, metadata={'optional': True})


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSampleKey(TypedKey['NullableElementsSample']):
    string_token: str = attr.ib(default=None, kw_only=True)
    bool_token: bool = attr.ib(default=None, kw_only=True)
    int_token: int = attr.ib(default=None, kw_only=True)
    local_date_token: LocalDate = attr.ib(default=None, kw_only=True)
    local_time_token: LocalTime = attr.ib(default=None, kw_only=True)
    local_minute_token: LocalMinute = attr.ib(default=None, kw_only=True)
    local_date_time_token: LocalDateTime = attr.ib(default=None, kw_only=True)
    enum_token: SampleEnum = attr.ib(default=None, kw_only=True)


@attr.s(slots=True, auto_attribs=True)
class NullableElementsSample(TypedRecord[NullableElementsSampleKey]):
    string_token: str = attr.ib(default=None, kw_only=True)
    bool_token: bool = attr.ib(default=None, kw_only=True)
    int_token: int = attr.ib(default=None, kw_only=True)
    local_date_token: LocalDate = attr.ib(default=None, kw_only=True)
    local_time_token: LocalTime = attr.ib(default=None, kw_only=True)
    local_minute_token: LocalMinute = attr.ib(default=None, kw_only=True)
    local_date_time_token: LocalDateTime = attr.ib(default=None, kw_only=True)
    enum_token: SampleEnum = attr.ib(default=None, kw_only=True)
    record_index: int = attr.ib(default=None, kw_only=True)
