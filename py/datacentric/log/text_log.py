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
from abc import ABC
from typing import List
from datacentric.primitive.string_util import StringUtil
from datacentric.log.log import Log
from datacentric.file_system.text_writer import TextWriter
from datacentric.log.log_entry import LogEntry


@attr.s(slots=True, auto_attribs=True)
class TextLog(Log, ABC):
    """Abstract base class of Log implementations that convert entries to text."""

    _text_writer: TextWriter = attr.ib(default=None, kw_only=True)
    """
    Text writer to which log output is directed.

    The value of this protected field must be set in derived classes
    before the log is used.
    """

    __indent_string: str = '  ' * 4

    def flush(self) -> None:
        """Flush data to permanent storage."""
        self._text_writer.flush()

    def publish_entry(self, log_entry: LogEntry) -> None:
        """
        Publish the specified entry to the log if log verbosity
        is the same or high as entry verbosity.

        When log entry data is passed to this method, only the following
        elements are required:

        * Verbosity
        * Title (should not have line breaks; if found will be replaced by spaces)
        * Description (line breaks and formatting will be preserved)

        The remaining fields of log_entry will be populated if the log
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

        # Do not record the log entry if entry verbosity exceeds log verbosity
        # Record all entries if log verbosity is not specified
        if log_entry.verbosity <= self.verbosity:

            # Title should not have line breaks if found will be replaced by spaces
            title_with_no_line_breaks: str = log_entry.title.replace(StringUtil.eol, ' ')
            formatted_title: str = f'{log_entry.verbosity.name}: {title_with_no_line_breaks}'
            self._text_writer.write_line(formatted_title)

            # Skip if description is not specified
            if log_entry.description:

                # Split the description into lines
                description_lines: List[str] = log_entry.description.split(StringUtil.eol)

                # Write lines with indent and remove the trailing blank line if any
                description_line_count: int = len(description_lines)
                i: int = 0
                description_line: str
                for description_line in description_lines:
                    i = i + 1

                    if not description_line:
                        if i < description_line_count - 1:
                            # Write empty line unless the empty token is last, in which
                            # case it represents the trailing EOL and including it would
                            # create in a trailing empty line not present in the original
                            # log message
                            self._text_writer.write_eol()
                    else:
                        # Write indent followed by description line
                        self._text_writer.write(self.__indent_string)
                        self._text_writer.write_line(description_line)
