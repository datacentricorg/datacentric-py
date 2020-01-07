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

from typing import TypeVar, Type
from pymongo import uri_parser

from datacentric import Data
from datacentric.primitive.string_util import StringUtil
from datacentric.storage.record import Record
from datacentric.storage.class_info import ClassInfo
from datacentric.storage.env_type import EnvType
from datacentric.storage.context import Context
from datacentric.storage.mongo.mongo_server import MongoServer
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource

TRecord = TypeVar('TRecord', bound=Record)


class RunCommand:
    def __init__(self, cli_args):
        self.source: str = cli_args.source
        self.env: EnvType = EnvType[cli_args.env]
        self.group: str = cli_args.group
        self.name: str = cli_args.name
        self.dataset: str = cli_args.dataset
        self.key: str = cli_args.key
        self.type: str = cli_args.type
        self.handler: str = cli_args.handler
        self.arguments = cli_args.arguments

    def execute(self):

        context = Context()

        data_source = TemporalMongoDataSource()
        data_source.env_type = self.env
        data_source.env_group = self.group
        data_source.env_name = self.name

        connection_literal = 'ConnectionString'
        connection = next((x for x in self.source.split(',') if x.startswith(connection_literal)), None)
        connection = connection[len(connection_literal) + 1:]
        if connection is not None:
            parsed_uri = uri_parser.parse_uri(connection)
            server_uri = ','.join(f'{x[0]}:{x[1]}' for x in parsed_uri['nodelist'])
            # TODO: mongodb+srv://?
            data_source.mongo_server = MongoServer.create_key(mongo_server_uri=f'mongodb://{server_uri}')

        data_source.init(context)

        common = data_source.get_common_or_none()
        if common is None:
            common = data_source.create_common()

        context.data_source = data_source
        context.data_set = common

        load_from = context.data_source.get_data_set(self.dataset, context.data_set)

        # Problem with importing types
        ClassInfo.get_derived_types('datacentric', Data)

        record_type: Type[TRecord] = ClassInfo.get_type(self.type)
        collection_type = ClassInfo.get_ultimate_base(record_type)
        record = context.data_source.load_by_key(record_type, f'{collection_type.__name__}={self.key}', load_from)
        handler_name = StringUtil.to_snake_case(self.handler)
        handler = getattr(record, handler_name, None)
        if handler is None:
            raise Exception(f'Type {record_type.__name__} does not have handler {handler_name}.')
        if not handler.handler:
            raise Exception(f'{handler_name} is not handler.')
        handler.__call__()
