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

from datacentric.file_system.text_writer import TextWriter


class FileWriter(TextWriter):
    """
    Implements TextWriter for writing to a file.
    """

    __slots__ = ('__file',)

    # __file: - TODO - specify type

    def __init__(self, path: str):
        """
        Open the specified file for writing.

        The argument is full path to the file.
        """

        # Open in mode that overwrites the context
        self.__file = open(file=path, mode="w")

    def write(self, value: object) -> None:
        """
        Write __str__ of the argument to the output stream.
        """
        print(value, end = '', file=self.__file)

    def write_line(self, value: object) -> None:
        """
        Write __str__ of the argument to the output stream, followed by EOL.
        """
        self.write(value)
        self.write_eol()

    def write_eol(self) -> None:
        """
        Write EOL to the output stream.
        """
        print(file=self.__file)

    def flush(self) -> None:
        """
        Flush buffer to the output stream.
        """
        self.__file.flush()

    def __del__(self):
        """
        Close the file.
        """
        self.__file.close()
