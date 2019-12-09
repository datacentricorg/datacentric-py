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

import unittest
import datetime as dt
from pymongo import MongoClient


class TestPyMongo(unittest.TestCase):
    """
    Test demonstrating how to use PyMongo driver API directly
    to write a record that follows DataCentric conventions.
    """

    def setUp(self):
        """
        Must call UnitTest constructor from setUp() method
        to avoid exception in properties of the base class.
        """
        UnitTest.__init__(self)

    def test_smoke(self):
        """Smoke test"""

        # Create connection
        client = MongoClient()
        db = client['TEST;PyMongoTest;Smoke']
        collection = db['NullableElementsSample']

        # Save record
        record = {'_id': '5de3ff042ef48d252cd1583c', '_t': ['Record', 'NullableElementsSample'],
                  '_dataset': '5de3ff042ef48d252cd15833',
                  '_key': 'A;true;123;12345678912345;2003-05-01;10:15:30.5;10:15;2003-05-01T10:15:30.5;'
                          '2003-05-01T10:15:30.5Z;EnumValue2',
                  'StringToken': 'A', 'BoolToken': True, 'IntToken': 123, 'LongToken': 12345678912345,
                  'LocalDateToken': 20030501, 'LocalTimeToken': 101530500, 'LocalMinuteToken': 1015,
                  'LocalDateTimeToken': 20030501101530500,
                  'InstantToken': dt.datetime.strptime('2003-05-01T10:15:30.500Z', '%Y-%m-%dT%H:%M:%S.%fZ'),
                  'EnumToken': 'EnumValue2'}
        collection.save(record)

        # Load record
        record = collection.find_one({'_key': 'A;true;123;12345678912345;2003-05-01;10:15:30.5;10:15;'
                                              '2003-05-01T10:15:30.5;2003-05-01T10:15:30.5Z;EnumValue2'})
        instant_token: dt.datetime = record['InstantToken']
        epoch: dt.datetime = dt.datetime.utcfromtimestamp(0)
        milliseconds_since_epoch = (instant_token - epoch).total_seconds() * 1000.0
        pass


if __name__ == "__main__":
    unittest.main()
