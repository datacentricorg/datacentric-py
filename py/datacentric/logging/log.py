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

from interface import implements, Interface
from abc import ABC, abstractmethod
from typing import Optional
from datacentric.logging.i_log import ILog, LogVerbosityEnum
from datacentric.logging.log_entry_type import LogEntryType
from datacentric.record.typed_key import TypedKey
from datacentric.record.typed_record import TypedRecord


class LogKey(TypedKey['Log']):
    """Key for Log."""

    __slots__ = ('log_name')

    log_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.log_name = None
        """Unique log name."""


class Log(TypedRecord[LogKey], ABC):
    """
    Log record implements ILog interface for recording log
    entries in a data source. Each log entry is a separate
    record.

    The log record serves as the key for querying log entries.
    To obtain the entire log, run a query for the Log element
    of the LogEntry record, then sort the entry records by
    their TemporalId.
    """

    __slots__ = ('log_name', 'verbosity')

    log_name: Optional[str]
    verbosity: LogVerbosityEnum

    def __init__(self):
        super().__init__()

        self.log_name = None
        """Unique log name."""

        self.verbosity = None
        """Minimal verbosity for which log entry will be displayed."""

    @abstractmethod
    def append(self, entry_type: LogEntryType, entry_sub_type: Optional[str], message: str,
               *message_params: object) -> None:
        """Append new entry to the log if entry type is the same or lower than log verbosity.
        Entry subtype is an optional tag in dot delimited format (specify null if no subtype).
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush log contents to permanent storage."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close log and release handle to permanent storage."""
        pass

    def exception(self, message: str, *message_params: object) -> Exception:
        """Record an error message and return exception with the same message.
        The caller is expected to raise the exception: raise Log.exception(message, messageParams)."""
        self.append(LogEntryType.Error, None, message, *message_params)
        e = Exception(message.format(message_params))
        return e

    def error(self, message: str, *message_params: object) -> None:
        """Record an error message and throw exception return by Log.exception(...)."""
        raise self.exception(message, *message_params)

    def warning(self, message: str, *message_params: object):
        """Record a warning."""
        self.append(LogEntryType.Warning, None, message, *message_params)

    def status(self, message: str, *message_params: object):
        """Record a status message."""
        self.append(LogEntryType.Status, None, message, *message_params)
