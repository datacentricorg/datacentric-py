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
from datacentric.io.file_writer import FileWriter
from datacentric.logging.text_log import TextLog
from datacentric.storage.context import Context


class FileLog(TextLog):
    """Writes log output to the specified text file as it arrives."""

    __slots__ = ('log_file_path',)

    log_file_path: Optional[str]

    def __init__(self):
        super().__init__()

        self.log_file_path = None
        """Log file path relative to output folder root."""

    def init(self, context: Context) -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method may be called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        IMPORTANT - Every override of this method must call base.Init()
        first, and only then execute the rest of the override method's code.
        """

        # Initialize base
        super().init(context)

        # Assign text writer for the log file
        self._text_writer = FileWriter(self.log_file_path)
