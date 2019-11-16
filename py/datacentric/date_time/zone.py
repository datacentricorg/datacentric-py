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
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord


class ZoneKey(TypedKey['Zone']):
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

    __slots__ = ('zone_name',)

    zone_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.zone_name = None
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


class Zone(TypedRecord[ZoneKey]):
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

    __slots__ = ('zone_name',)

    zone_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.zone_name = None
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