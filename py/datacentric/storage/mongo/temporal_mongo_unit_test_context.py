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

from datacentric.storage.mongo.mongo_unit_test_context import MongoUnitTestContext
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource


class TemporalMongoUnitTestContext(MongoUnitTestContext[TemporalMongoDataSource]):
    """
    Specialization of MongoUnitTestContext for TemporalMongoDataSource.

    MongoUnitTestContext is the context for use in test fixtures that
    require a data source, parameterized by data source type.
    It extends UnitTestContext by creating an empty test
    database specific to the test method, and deleting
    it after the test exits. The context creates Common
    dataset in the database and assigns its TemporalId to
    the DataSet property of the context.

    If the test sets KeepTestData = true, the data is retained
    after the text exits. This data will be cleared on the
    next launch of the test.

    For tests that do not require a data source, use UnitTestContext.
    """

    __slots__ = ()

    def __init__(self):
        """Inspect call stack to set properties."""
        super().__init__()
