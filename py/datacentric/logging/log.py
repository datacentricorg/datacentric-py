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
from datacentric.logging.log_entry import LogEntry
from datacentric.logging.log_verbosity import LogVerbosity
from datacentric.record.typed_key import TypedKey
from datacentric.record.typed_record import TypedRecord


class LogKey(TypedKey['Log']):
    """
    Provides a unified API for writing log output to:

    * Console
    * String
    * File
    * Database
    * Logging frameworks such as log4net and other logging frameworks
    * Cloud logging services such as AWS CloudWatch
    """

    __slots__ = ('log_name')

    log_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.log_name = None
        """Unique log name."""


class Log(TypedRecord[LogKey], ABC):
    """
    Provides a unified API for writing log output to:

    * Console
    * String
    * File
    * Database
    * Logging frameworks such as log4net and other logging frameworks
    * Cloud logging services such as AWS CloudWatch
    """

    __slots__ = ('log_name', 'verbosity')

    log_name: Optional[str]
    verbosity: Optional[LogVerbosity]

    def __init__(self):
        super().__init__()

        self.log_name = None
        """Unique log name."""

        self.verbosity = None
        """Minimal verbosity for which log entry will be displayed."""

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

        # If verbosity is None, set to Error
        # if verbosity is None TODO - fix
        #    verbosity = LogVerbosity.Error

    @abstractmethod
    def flush(self) -> None:
        """Flush data to permanent storage."""
        pass

    @abstractmethod
    def publish_entry(self, log_entry: LogEntry) -> None:
        """
        Publish the specified entry to the log if log verbosity
        is the same or high as entry verbosity.

        When log entry data is passed to this method, only the following
        elements are required:

        * Verbosity
        * Title (should not have line breaks; if found will be replaced by spaces)
        * Description (line breaks and formatting will be preserved)

        The remaining fields of LogEntry will be populated if the log
        entry is published to a data source. They are not necessary if the
        log entry is published to a text log.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Info: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """
        pass

    def publish(self, verbosity: LogVerbosity, title: str, description: str = None) -> None:
        """
        Publish a new entry to the log if log verbosity
        is the same or high as entry verbosity.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Info: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """

        # Populate only those fields of of the log entry that are passed to this method.
        # The remaining fields will be populated if the log entry is published to a data
        # source. They are not necessary if the log entry is published to a text log.
        log_entry = LogEntry()
        log_entry.verbosity = verbosity
        log_entry.title = title
        log_entry.description = description

        # Publish the log entry to the log
        self.publish_entry(log_entry)
