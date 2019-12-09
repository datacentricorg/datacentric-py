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

import sys
import os
from typing import Optional
from datacentric.storage.context import Context
from datacentric.log.log_verbosity import LogVerbosity
from datacentric.log.file_log import FileLog


class UnitTestContext(Context):
    """
    Context for use in test fixtures that do not require a data
    source. Attempting to access DataSource property using this
    context will cause an error.

    This class extends Context with approval test functionality.
    """

    __slots__ = ('test_method_name', 'test_module_name', 'test_folder_path')

    test_method_name: Optional[str]
    test_module_name: Optional[str]
    test_folder_path: Optional[str]

    def __init__(self):
        """Inspect call stack to set properties."""
        super().__init__()

        self.test_method_name = None
        """
        Name of the unit test method obtained by inspecting call stack.
        """

        self.test_module_name = None
        """
        Test module name obtained by inspecting call stack.
        """

        self.test_folder_path = None
        """
        Test folder name obtained by inspecting call stack.
        """

        # Inspect call stack to get filename and method name of the
        # source code location where UnitTestContext constructor is called.
        # The location we are looking for is the first one that is
        # not inside an __init__ method.
        stack_frame_index: int = 1
        while True:
            caller_frame = sys._getframe(stack_frame_index)
            if caller_frame.f_code.co_name != '__init__':
                break
            stack_frame_index = stack_frame_index + 1

        # Get method name from call stack
        self.test_method_name = caller_frame.f_code.co_name

        # Use right split (rsplit) to get folder path and module name
        test_file_path: str = caller_frame.f_code.co_filename
        self.test_folder_path, test_module_name_with_extension = os.path.split(test_file_path)
        self.test_module_name = test_module_name_with_extension.replace('.py', '')

        # Use log file name format class_name.method_name.approved.txt from
        # the ApprovalTests.Python package
        log_file_path: str = os.path.join(self.test_folder_path,
                                          f'{self.test_module_name}.{self.test_method_name}.approved.txt')

        # Create file log for log_file_path
        # Do not call init(...) here as it
        # will be initialized by the context
        # property setter
        file_log: FileLog = FileLog()
        file_log.log_file_path = log_file_path
        self.log = file_log

        # Increase log verbosity to Verify from its
        # default level set in base class Context.
        #
        # DO NOT move this to FileLog initialization
        # as it will get reset when log.init(...)
        # is called by Context.log setter.
        self.log.verbosity = LogVerbosity.Verify
