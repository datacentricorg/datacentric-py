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

import argparse
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

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(help='commands', dest='command')

# Schema command
schema_parser = sub_parsers.add_parser('schema', help='Write schema to data source.')
schema_parser.add_argument('--packages', '-p', nargs='+', required=True, help='Generate schema from provided packages')
# Change short option to avoid -h conflict. Users always expect -h to work
schema_parser.add_argument('--host', '-o', type=str, required=False,
                           help='Db Host. Fallbacks to standard if not provided')
schema_parser.add_argument('--env', '-e', type=str, required=True, help='Environment type')
schema_parser.add_argument('--group', '-g', type=str, required=True, help='Environment group')
schema_parser.add_argument('--name', '-n', type=str, required=True, help='Environment name')

# Run command
run_parser = sub_parsers.add_parser('run', help='Execute handler')
run_parser.add_argument('--source', '-s', required=True,
                        help='Source environment - folder for file storage and connection string for DB.')
run_parser.add_argument('--env', '-e', type=str, required=True, help='Environment type')
run_parser.add_argument('--group', '-g', type=str, required=True, help='Environment group')
run_parser.add_argument('--name', '-n', type=str, required=True, help='Environment name')
run_parser.add_argument('--dataset', '-d', required=True, help='Setting specifies data set name.')
run_parser.add_argument('--key', '-k', required=True, help='Key of entity.')
run_parser.add_argument('--type', '-t', required=True, help='Type handler belongs.')
# Change short option to avoid -h conflict. Users always expect -h to work
run_parser.add_argument('--handler', '-l', required=True, help='Handler name to execute.')
run_parser.add_argument('--arguments', '-a', help='Space separated handler arguments in name=value format.')


def schema(args):
    context = Context()

    data_source = TemporalMongoDataSource()
    data_source.env_type = EnvType[args.env]
    data_source.env_group = args.group
    data_source.env_name = args.name
    if args.host is not None:
        data_source.mongo_server = MongoServer.create_key(mongo_server_uri=args.host)
    data_source.init(context)

    common = data_source.get_common_or_none()
    if common is None:
        common = data_source.create_common()

    context.data_source = data_source
    context.data_set = common

    datas = ClassInfo.get_derived_types('datacentric', Data)
    enums = ClassInfo.get_derived_types('datacentric', IntEnum)
    type_declarations = [to_type_declaration(x) for x in datas]
    enum_declarations = [to_enum_declaration(x) for x in enums]

    # Save declarations to db
    context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
    context.data_source.save_many(EnumDecl, enum_declarations, context.data_set)


def run(args):
    pass


if __name__ == '__main__':
    res = parser.parse_args()
    command = res.command
    if command == 'schema':
        schema(res)
    elif command == 'run':
        run(res)
    else:
        print(f'Unknown command: {command}.')
        parser.print_help()
