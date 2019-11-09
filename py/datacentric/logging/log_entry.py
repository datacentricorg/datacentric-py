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

from datacentric.record.typed_key import TypedKey
from datacentric.record.typed_record import TypedRecord
from datacentric.logging.log_entry_type import LogEntryType


class LogEntryKey(TypedKey['LogEntry']):
    """Key for LogEntry."""

    __slots__ = ('id')


    def __init__(self):
        super().__init__()



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

    log: LogKey
    verbosity: LogVerbosityEnum
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
    def __str__(self):
        return self._entry_text

    @staticmethod
    def format_message(message: str, *message_params: object) -> str:
        if len(message_params) > 0:
            formatted_message_params = []
            for arg in message_params:
                arg_str = str(arg)

                # Restrict message length if more than max length
                if len(arg_str) > LogEntry.__max_message_param_length:
                    substring_length: int = (LogEntry.__max_message_param_length - 5) // 2
                    head = arg_str[0:substring_length]
                    tail = arg_str[len(arg_str) - substring_length:len(arg_str)]
                    arg_str = head + ' ... ' + tail
                formatted_message_params.append(arg_str)

            result = message.format(formatted_message_params)

            # If the message ends with four dots (....) because the last argument is truncated
            # while its token is followed by a dot (.), reduce to three dots at the end (...)
            if result.endswith('....'):
                return result[0: len(result) - 1]

            return result

        # Do not perform substitution if no parameters are specified.
        # This will work even if the string contains {} characters
        else:
            return message