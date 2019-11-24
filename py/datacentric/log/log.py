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
from abc import ABC, abstractmethod
from datacentric.storage.context import Context
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord
from datacentric.log.log_verbosity import LogVerbosity
from datacentric.log.log_entry import LogEntry


@attr.s(slots=True, auto_attribs=True)
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

    log_name: str = attr.ib(default=None, kw_only=True)
    """Unique log name."""


@attr.s(slots=True, auto_attribs=True)
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

    log_name: str = attr.ib(default=None, kw_only=True)
    """Unique log name."""

    verbosity: LogVerbosity = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """Minimal verbosity for which log entry will be displayed."""

    def init(self, context: Context) -> None:
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
        if self.verbosity is None:
            self.verbosity = LogVerbosity.Error

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

    def error(self, title: str, description: str = None) -> None:
        """
        Publish an error message to the log for any log verbosity.

        This method does not throw an exception; it is invoked
        to indicate an error when exception is not necessary,
        and it may also be invoked when the exception is caught.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Error: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """
        self.publish(LogVerbosity.Error, title, description)

    def warning(self, title: str, description: str = None) -> None:
        """
        Publish a warning message to the log if log verbosity
        is at least Warning.

        Warning messages should be used sparingly to avoid
        flooding log output with insignificant warnings.
        A warning message should never be generated inside
        a loop.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Warning: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """
        self.publish(LogVerbosity.Warning, title, description)

    def info(self, title: str, description: str = None) -> None:
        """
        Publish an info message to the log if log verbosity
        is at least Info.

        Info messages should be used sparingly to avoid
        flooding log output with superfluous data. An info
        message should never be generated inside a loop.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Info: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """
        self.publish(LogVerbosity.Info, title, description)

    def verify(self, title: str, description: str = None) -> None:
        """
        Publish a verification message to the log if log verbosity
        is at least Verify.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Verify: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """
        self.publish(LogVerbosity.Verify, title, description)

    def assert_(self, condition: bool, title: str, description: str = None) -> None:
        """
        If condition is false, record an error message for any
        verbosity. If condition is true, record a verification
        message to the log if log verbosity is at least Verify.

        In a text log, the first line of each log entry is Verbosity
        followed by semicolon separator and then Title of the log entry.
        Remaining lines are Description of the log entry recorded with
        4 space indent but otherwise preserving its formatting.

        Example:

        Verify: Sample Title
            Sample Description Line 1
            Sample Description Line 2
        """

        # Records a log entry for any verbosity if condition is false,
        # but requires at least Verify verbosity if condition is true
        if condition:
            self.error(title, description)
        else:
            self.verify(title, description)
