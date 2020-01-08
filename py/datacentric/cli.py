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

from datacentric.commands.run import RunCommand
from datacentric.commands.schema import SchemaCommand

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(help='commands', dest='command')

# Schema command
schema_parser = sub_parsers.add_parser('schema', help='Write schema to data source.')
SchemaCommand.add_arguments(schema_parser)

# Run command
run_parser = sub_parsers.add_parser('run', help='Execute handler')
RunCommand.add_arguments(run_parser)

if __name__ == '__main__':
    res = parser.parse_args()
    command = res.command
    if command == 'schema':
        schema = SchemaCommand(res)
        schema.execute()
    elif command == 'run':
        run = RunCommand(res)
        run.execute()
    else:
        print(f'Unknown command: {command}.')
        parser.print_help()
