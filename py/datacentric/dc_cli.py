import argparse
from enum import IntEnum

from bson import ObjectId

from datacentric.storage.env_type import EnvType
from datacentric.storage.context import Context
from datacentric.storage.data import Data
from datacentric.storage.mongo.mongo_server import MongoServer
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.schema.declaration.type_decl import TypeDecl
from datacentric.schema.declaration.enum_decl import EnumDecl
from datacentric.schema.generator import to_type_declaration, to_enum_declaration, get_derived_types

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(help='commands', dest='command')

# Schema command
schema_parser = sub_parsers.add_parser('schema', help='Write schema to data source.')
schema_parser.add_argument('--package', '-p', nargs='+', required=True, help='Generate schema from provided packages')
# Change short option to avoid -h conflict. Users always expect -h to work
schema_parser.add_argument('--host', '-o', type=str, required=False,
                           help='Db Host. Fallbacks to standard if not provided')
schema_parser.add_argument('--env', '-e', type=str, required=True, help='Environment type')
schema_parser.add_argument('--group', '-g', type=str, required=True, help='Environment group')
schema_parser.add_argument('--name', '-n', type=str, required=True, help='Environment name')


def schema(args):
    context = Context()
    # if args.host is not None:
    #     server = MongoServer.create_key(mongo_server_uri=args.host)
    # else:
    #     server = None
    # data_source = TemporalMongoDataSource(env_type=EnvType[args.env], env_group=args.group, env_name=args.name,
    #                                       mongo_server=server)

    data_source = TemporalMongoDataSource()
    data_source.env_type = EnvType[args.env]
    data_source.env_group = args.group
    data_source.env_name = args.name
    if args.host is not None:
        data_source.mongo_server = MongoServer.create_key(mongo_server_uri=args.host)
    # TODO: Extend data_source with get_common_or_none

    data_source.init(context)
    common = data_source.get_data_set_or_none('Common', ObjectId('000000000000000000000000'))
    if common is None:
        common = data_source.create_common()
    context.data_source = data_source
    context.data_set = common

    type_declarations = [to_type_declaration(x) for x in get_derived_types('datacentric', Data)]
    enum_declarations = [to_enum_declaration(x) for x in get_derived_types('datacentric', IntEnum)]

    # Save declarations to db
    context.data_source.save_many(TypeDecl, type_declarations, context.data_set)
    context.data_source.save_many(EnumDecl, enum_declarations, context.data_set)


if __name__ == '__main__':
    res = parser.parse_args()
    print(res)
    if res.command == 'schema':
        schema(res)
