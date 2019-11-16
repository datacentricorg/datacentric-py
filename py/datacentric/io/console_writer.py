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

from datacentric.io.text_writer import TextWriter

class ConsoleWriter(TextWriter):
    """
    Implements TextWriter for writing to the console.
    """

    def write(self, value: object) -> None:
        """
        Write __str__ of the argument to the output stream.
        """
        print(value)

    def write_line(self, value: object) -> None:
        """
        Write __str__ of the argument to the output stream, followed by EOL.
        """
        self.write(value)
        print()

    def flush(self) -> None:
        """
        Flush buffer to the output stream.
        """

        # Do nothing
        pass