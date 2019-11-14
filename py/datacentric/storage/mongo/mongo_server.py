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
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord


class MongoServerKey(TypedKey['MongoServer']):
    """
    Provides Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """

    __slots__ = ('mongo_server_uri',)

    mongo_server_uri: Optional[str]

    def __init__(self):
        super().__init__()

        self.mongo_server_uri = None
        """
        Mongo server URI.

        Server URI specified here must refer to the entire server, not
        an individual database.
        """


class MongoServer(TypedRecord[MongoServerKey]):
    """
    Provides Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """

    __slots__ = ('mongo_server_uri',)

    mongo_server_uri: Optional[str]

    def __init__(self):
        super().__init__()

        self.mongo_server_uri = None
        """
        Mongo server URI.

        Server URI specified here must refer to the entire server, not
        an individual database.
        """
