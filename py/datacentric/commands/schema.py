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

from enum import IntEnum

from datacentric.storage.class_info import ClassInfo
from datacentric.storage.env_type import EnvType
from datacentric.storage.context import Context
from datacentric.storage.data import Data
from datacentric.storage.mongo.mongo_server import MongoServer
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.schema.declaration.type_decl import TypeDecl
from datacentric.schema.declaration.enum_decl import EnumDecl
from datacentric.schema.generator import to_type_declaration, to_enum_declaration


class SchemaCommand:
    """Command to write packages schema to specified data source"""

    def __init__(self, cli_args):
        """Init schema command from parsed CLI args."""
        self.packages: str = cli_args.packages
        self.host: str = cli_args.host
        self.env: EnvType = EnvType[cli_args.env]
        self.group: str = cli_args.group
        self.name: str = cli_args.name

    @classmethod
    def add_arguments(cls, parser):
        """Add arguments to parser."""
        parser.add_argument('--packages', '-p', nargs='+', required=True,
                            help='Generate schema from provided packages')
        # Change short option to avoid -h conflict. Users always expect -h to work
        parser.add_argument('--host', '-o', type=str, required=False,
                            help='Db Host. Fallbacks to standard if not provided')
        parser.add_argument('--env', '-e', type=str, required=True, help='Environment type')
        parser.add_argument('--group', '-g', type=str, required=True, help='Environment group')
        parser.add_argument('--name', '-n', type=str, required=True, help='Environment name')

    def execute(self):
        """Generate declarations for packages and save to data source."""
        context = Context()

        data_source = TemporalMongoDataSource()
        data_source.env_type = self.env
        data_source.env_group = self.group
        data_source.env_name = self.name
        if self.host is not None:
            data_source.mongo_server = MongoServer.create_key(mongo_server_uri=self.host)
        data_source.init(context)

        common = data_source.get_common_or_none()
        if common is None:
            common = data_source.create_common()

        context.data_source = data_source
        context.data_set = common

        for package in self.packages:
            datas = ClassInfo.get_derived_types(package, Data)
            enums = ClassInfo.get_derived_types(package, IntEnum)
            type_declarations = [to_type_declaration(x) for x in datas]
            enum_declarations = [to_enum_declaration(x) for x in enums]

            # Save declarations to db
            context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
            context.data_source.save_many(EnumDecl, enum_declarations, context.data_set)
