#  Copyright (C) 2013-present The DataCentric Authors.
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#     http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import unittest

from bson import ObjectId
from pymongo.database import Database
from pymongo import DESCENDING, ASCENDING

from datacentric import TemporalMongoUnitTestContext, Context
from datacentric.log.console_log import ConsoleLog


class TestMongoPerformance(unittest.TestCase):
    RECORD_COUNT = 10  # 300_000
    DATASET_COUNT = 2  # 10
    VERSION_COUNT = 2  # 10
    ARRAY_SIZE = 10  # 1_000

    def get_db(self, context: Context) -> Database:
        return context.data_source.db

    def insert_records_a(self, context: Context):
        """Insert N non-versioned instances."""
        db = self.get_db(context)
        records = []
        for i in range(TestMongoPerformance.RECORD_COUNT):
            rec = {'_id': 'KeyPrefix' + str(i),
                   'DoubleElement': float(i),
                   'IntElement': i,
                   'VersionElement': 0}
            if TestMongoPerformance.ARRAY_SIZE > 0:
                rec['ArrayElement'] = [float(x) for x in range(TestMongoPerformance.ARRAY_SIZE)]
            records.append(rec)

        # Unique index on _id is created automatically
        collection = db.get_collection('A')
        collection.create_index([('DoubleElement', DESCENDING)])
        collection.insert_many(records)
        context.log.verify(f'Inserted {TestMongoPerformance.RECORD_COUNT} records.')

    def insert_records_b(self, context: Context):
        """Insert M copies of each of N versioned instances B."""
        db = self.get_db(context)
        coll = db.get_collection('B')
        coll.create_index([('KeyElement', ASCENDING), ('_id', DESCENDING), ('DataSet', DESCENDING)])

        records = []
        for data_set_idx in range(TestMongoPerformance.DATASET_COUNT):
            dataset = ObjectId()
            for version_idx in range(TestMongoPerformance.VERSION_COUNT):
                for record_idx in range(TestMongoPerformance.RECORD_COUNT):
                    rec = {'_id': ObjectId(),
                           'DataSet': dataset,
                           'KeyElement': 'KeyPrefix=' + str(record_idx),
                           'StringElement1': str(record_idx % 2),
                           'StringElement2': str(record_idx % 2),
                           'DoubleElement': float(record_idx),
                           'IntElement': record_idx,
                           'VersionElement': version_idx}
                    if TestMongoPerformance.ARRAY_SIZE > 0:
                        rec['ArrayElement'] = [float(x) for x in range(TestMongoPerformance.ARRAY_SIZE)]
                    records.append(rec)
        coll.insert_many(records)
        context.log.verify(f'Inserted {TestMongoPerformance.RECORD_COUNT} records.')

    def test_insert_a(self):
        with TemporalMongoUnitTestContext() as context:
            self.insert_records_a(context)

    def test_insert_b(self):
        with TemporalMongoUnitTestContext() as context:
            self.insert_records_b(context)
