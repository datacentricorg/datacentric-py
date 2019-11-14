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
from bson import ObjectId
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord
from datacentric.logging.log_verbosity import LogVerbosity

# To prevent linter error on type hint in quotes
if False:
    from datacentric.storage.context import Context
    from datacentric.logging.log import LogKey


class LogEntryKey(TypedKey['LogEntry']):
    """
    Contains a single entry (message) in a log.

    The Log record serves as the key for querying LogEntry records.
    To obtain the entire log, run a query for the Log element of
    the LogEntry record, then sort the entry records by their TemporalId.

    Derive from this class to provide specialized LogEntry subtypes
    that include additional data.
    """

    __slots__ = ('id',)

    id_: ObjectId

    def __init__(self):
        super().__init__()

        self.id_ = None
        """
        Defining element Id here includes the record's TemporalId
        in its key. Because TemporalId of the record is specific
        to its version, this is equivalent to using an auto-
        incrementing column as part of the record's primary key
        in a relational database.

        For the record's history to be captured correctly, all
        update operations must assign a new TemporalId with the
        timestamp that matches update time.
        """


class LogEntry(TypedRecord[LogEntryKey]):
    """
    Contains a single entry (message) in a log.

    The Log record serves as the key for querying LogEntry records.
    To obtain the entire log, run a query for the Log element of
    the LogEntry record, then sort the entry records by their TemporalId.

    Derive from this class to provide specialized LogEntry subtypes
    that include additional data.
    """

    __slots__ = ('log', 'verbosity', 'title', 'description')

    log: Optional['LogKey']
    verbosity: Optional[LogVerbosity]
    title: Optional[str]
    description: Optional[str]

    def __init__(self):
        super().__init__()

        self.log = None
        """
        Log for which the entry is recorded.

        To obtain the entire log, run a query for the Log element of
        the entry record, then sort the entry records by their TemporalId.
        """

        self.verbosity = None
        """Minimal verbosity for which log entry will be displayed."""

        self.title = None
        """
        Short, single-line title of the log entry.

        Line breaks in title will be replaced by spaces when the
        log entry is displayed.
        """

        self.description = None
        """
        Optional single-line or multi-line description of the log entry.

        Line breaks, whitespace and other formatting in the description
        will be preserved when the log entry is displayed.
        """

    def init(self, context: 'Context') -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method may be called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        IMPORTANT - Every override of this method must call base.Init()
        first, and only then execute the rest of the override method's code.
        """

        # Initialize base before executing the rest of the code in this method
        super().init(context)

        # TODO - add validation code

    def __str__(self):
        """
        Returns verbosity followed by semicolon and then title
        with line breaks replaced by spaces, for example:

        Info: Sample Info Message
        """
        # TODO - provide correct format
        return self.title
