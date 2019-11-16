import datetime as dt
from enum import Enum
from typing import List, Optional

from datacentric.date_time.local_date import LocalDate
from datacentric.date_time.local_time import LocalTime
from datacentric.date_time.local_minute import LocalMinute
from datacentric.date_time.local_date_time import LocalDateTime
from datacentric.storage.typed_record import TypedRecord
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.data import Data


class ElementSample(Data):
    __slots__ = ['double_element3', 'string_element3']
    double_element3: Optional[float]
    string_element3: Optional[str]

    def __init__(self):
        super().__init__()
        self.double_element3 = None
        self.string_element3 = None


class SampleEnum(Enum):
    Empty = 0
    EnumValue1 = 1
    EnumValue2 = 2


class BaseSample(TypedRecord['BaseSampleKey']):
    __slots__ = ['record_id',
                 'record_index',
                 'double_element',
                 'local_date_element',
                 'local_time_element',
                 'local_minute_element',
                 'local_date_time_element',
                 'enum_value',
                 'version']
    record_id: Optional[str]
    record_index: Optional[int]
    double_element: Optional[float]
    local_date_element: Optional[dt.date]
    local_time_element: Optional[dt.time]
    local_minute_element: Optional[LocalMinute]
    local_date_time_element: Optional[dt.datetime]
    enum_value: Optional[SampleEnum]
    version: Optional[int]

    def __init__(self):
        super().__init__()
        self.record_id = None
        self.record_index = None
        self.double_element = None
        self.local_date_element = None
        self.local_time_element = None
        self.local_minute_element = None
        self.local_date_time_element = None
        self.enum_value = None
        self.version = None


class BaseSampleKey(TypedKey[BaseSample]):
    __slots__ = ['record_id', 'record_index']

    record_id: Optional[str]
    record_index: Optional[int]

    def __init__(self):
        super().__init__()
        self.record_id = None
        self.record_index = None


class DerivedSample(BaseSample):
    __slots__ = ['double_element2', 'string_element2', 'list_of_string', 'list_of_double', 'list_of_nullable_double',
                 'data_element', 'data_element_list', 'key_element', 'key_element_list']
    double_element2: Optional[float]
    string_element2: Optional[str]
    list_of_string: Optional[List[Optional[str]]]
    list_of_double: Optional[List[float]]
    list_of_nullable_double: Optional[List[Optional[float]]]
    data_element: Optional[ElementSample]
    data_element_list:  Optional[List[Optional[ElementSample]]]
    key_element: Optional[BaseSampleKey]
    key_element_list:  Optional[List[Optional[BaseSampleKey]]]

    def __init__(self):
        super().__init__()
        self.double_element2 = None
        self.string_element2 = None
        self.list_of_string = None
        self.list_of_double = None
        self.list_of_nullable_double = None
        self.data_element = None
        self.data_element_list = None
        self.key_element = None
        self.key_element_list = None


class NullableElementsSampleKey(TypedKey['NullableElementsSample']):
    __slots__ = ['string_token', 'bool_token', 'int_token', 'local_date_token', 'local_time_token',
                 'local_minute_token', 'local_date_time_token', 'enum_token']
    string_token: Optional[str]
    bool_token: Optional[bool]
    int_token: Optional[int]
    local_date_token: Optional[LocalDate]
    local_time_token: Optional[LocalTime]
    local_minute_token: Optional[LocalMinute]
    local_date_time_token: Optional[LocalDateTime]
    enum_token: Optional[SampleEnum]

    def __init__(self):
        super().__init__()
        self.string_token = None
        self.bool_token = None
        self.int_token = None
        self.local_date_token = None
        self.local_time_token = None
        self.local_minute_token = None
        self.local_date_time_token = None
        self.enum_token = None


class NullableElementsSample(TypedRecord[NullableElementsSampleKey]):
    __slots__ = ['string_token', 'bool_token', 'int_token', 'local_date_token', 'local_time_token',
                 'local_minute_token', 'local_date_time_token', 'enum_token', 'record_index']
    string_token: Optional[str]
    bool_token: Optional[bool]
    int_token: Optional[int]
    local_date_token: Optional[LocalDate]
    local_time_token: Optional[LocalTime]
    local_minute_token: Optional[LocalMinute]
    local_date_time_token: Optional[LocalDateTime]
    enum_token: Optional[SampleEnum]
    record_index: Optional[int]

    def __init__(self):
        super().__init__()
        self.string_token = None
        self.bool_token = None
        self.int_token = None
        self.local_date_token = None
        self.local_time_token = None
        self.local_minute_token = None
        self.local_date_time_token = None
        self.enum_token = None
        self.record_index = None
