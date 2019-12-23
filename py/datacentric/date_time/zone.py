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
from typing import Union
import datetime as dt
import pytz
from datacentric.storage.record import Record
from datacentric.date_time.zone_key import ZoneKey


@attr.s(slots=True, auto_attribs=True)
class Zone(Record):
    """
    This class provides timezone conversion between UTC
    and local datetime for the specified timezone.

    Only the following timezone names are permitted:

    * UTC; and
    * IANA city timezones such as America/New_York

    Other 3-letter regional timezones such as EST or EDT are
    not permitted because they do not handle the transition
    between winter and summer time automatically for those
    regions where winter time is defined.

    Because ZoneName is used to look up timezone conventions,
    it must match either the string UTC or the code in IANA
    timezone database precisely. The IANA city timezone code
    has two slash-delimited tokens, the first referencing the
    country and the other the city, for example America/New_York.
    """

    zone_name: str = attr.ib(default=None, kw_only=True)
    """
    Unique timezone name.

    Only the following timezone names are permitted:

    * UTC; and
    * IANA city timezones such as America/New_York

    Other 3-letter regional timezones such as EST or EDT are
    not permitted because they do not handle the transition
    between winter and summer time automatically for those
    regions where winter time is defined.

    Because ZoneName is used to look up timezone conventions,
    it must match either the string UTC or the code in IANA
    timezone database precisely. The IANA city timezone code
    has two slash-delimited tokens, the first referencing the
    country and the other the city, for example America/New_York.
    """

    # --- METHODS

    def to_key(self) -> str:
        """Get Zone key."""
        return 'Zone=' + self.zone_name

    @classmethod
    def create_key(cls, *, zone_name: str) -> str:
        """Create Zone key."""
        return 'Zone=' + zone_name

    # --- CLASS

    @classmethod
    def get_zone_name_from_key(cls, key: str) -> str:
        """Get zone_name by parsing key."""
        return key.split('=', 1)[1].split(';')[0]

    @classmethod
    def get_tzinfo_from_key(cls, key: str) -> dt.tzinfo:
        """Get tzinfo object by parsing key, without loading the zone record."""
        zone_name: str = cls.get_zone_name_from_key(key)
        return pytz.timezone(zone_name)
