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

from datacentric.storage.context import Context
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.storage.env_type import EnvType


class TemporalMongoUnitTestContext:
    def __init__(self, test):
        self.test = test

    def __enter__(self):
        context = Context()

        source = TemporalMongoDataSource()
        source.env_type = EnvType.Test
        source.env_group = self.test.id().split('.')[-2]
        source.env_name = self.test.id().split('.')[-1]
        source.init(context)

        context.data_source = source
        context.data_set = context.data_source.create_common()

        return context

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit tests context')
