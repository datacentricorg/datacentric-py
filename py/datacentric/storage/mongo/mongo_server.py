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
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.typed_record import TypedRecord


class MongoServerKeyHint:
    """Type hint indicating that str represents MongoServerKey."""
    pass


@attr.s(slots=True, auto_attribs=True)
class MongoServerKey(TypedKey['MongoServer']):
    """
    Provides Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """

    mongo_server_uri: str = attr.ib(default=None, kw_only=True)
    """
    Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """


@attr.s(slots=True, auto_attribs=True)
class MongoServer(TypedRecord[MongoServerKey]):
    """
    Provides Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """

    mongo_server_uri: str = attr.ib(default=None, kw_only=True)
    """
    Mongo server URI.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """
