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

    def __init__(self):
        super().__init__()
        # Inspect stack to get filename and method name of the source
        # code location where UnitTestContext constructor is called.
        # If called from create_method_context, take the method that
        # called create_method_context instead.
        stack_frame_index: int = 1
        while True:
            caller_frame = sys._getframe(stack_frame_index)
            if caller_frame.f_code.co_name != 'create_method_context':
                break
            stack_frame_index = stack_frame_index + 1

        test_file_path: str = caller_frame.f_code.co_filename
        method_name: str = caller_frame.f_code.co_name

        # Use log file name format class_name.method_name.approved.txt from
        # the ApprovalTests.Python package
        test_file_path_without_extension: str = test_file_path.replace('.py', '')
        log_file_path: str = f'{test_file_path_without_extension}.{method_name}.approved.txt'

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
