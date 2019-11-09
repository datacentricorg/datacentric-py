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
from typing import Optional
from datacentric.logging.i_log import ILog


class IContext(Interface):
    """
    Context interface provides:

    * Default data source
    * Default dataset of the default data source
    * Logging
    * Progress reporting
    * Filesystem access (if available)
    """

    def get_log(self) -> ILog:
        pass
