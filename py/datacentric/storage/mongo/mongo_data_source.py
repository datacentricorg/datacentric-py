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
from abc import ABC
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from datacentric.storage.mongo.mongo_server import MongoServerKey
from datacentric.storage.context import Context
from datacentric.storage.data_source import DataSource
from datacentric.storage.env_type import EnvType


@attr.s(slots=True, auto_attribs=True)
class MongoDataSource(DataSource, ABC):
    """
    Abstract base class for data source implementations based on MongoDB.

    This class provides functionality shared by all MongoDB data source types.
    """

    mongo_server: MongoServerKey = attr.ib(default=None, kw_only=True, metadata={'optional': True})
    """
    Specifies Mongo server for this data source.

    Defaults to local server on the standard port if not specified.

    Server URI specified here must refer to the entire server, not
    an individual database.
    """

    __prohibited_symbols = '/\\. "$*<>:|?'
    __max_db_name_length = 64

    __env_type: EnvType = attr.ib(default=None, init=False)
    __db: Database = attr.ib(default=None, init=False)
    __db_name: str = attr.ib(default=None, init=False)
    __client: MongoClient = attr.ib(default=None, init=False)
    __prev_object_id: ObjectId = attr.ib(default=DataSource._empty_id, init=False)

    def init(self, context: Context) -> None:
        """Set context and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        Connects to mongo server and picks database defined by db_name.
        """

        # Initialize base before executing the rest of the code in this method
        super().init(context)

        # perform database name validation
        if self.env_type == EnvType.Empty:
            raise Exception('DB instance type is not specified.')
        if not self.env_group:
            raise Exception('DB instance name is not specified.')
        if not self.env_name:
            raise Exception('DB environment name is not specified.')

        self.__env_type = self.env_type

        if self.__env_type in [EnvType.Prod, EnvType.Uat, EnvType.Dev, EnvType.Test]:
            self.__db_name = ';'.join([self.__env_type.name.upper(), self.env_group, self.env_name])
        elif self.__env_type == EnvType.Custom:
            if self.env_group is not None or self.env_group == '':
                raise Exception(f'env_group={self.env_group} is specified, but '
                                f'should be empty for Custom environment type.')
            self.__db_name = self.env_name
        elif self.__env_type == EnvType.Empty:
            raise Exception(f'EnvType is empty for DataSourceName={self.data_source_name}.')
        else:
            raise Exception(f'Unknown env_type={self.__env_type}.')

        if any(x in self.__db_name for x in MongoDataSource.__prohibited_symbols):
            raise Exception(f'MongoDB database name {self.__db_name} contains a space or another '
                            f'prohibited character from the following list: /\\.\"$*<>:|?')

        if len(self.__db_name) > MongoDataSource.__max_db_name_length:
            raise Exception(f'MongoDB database name {self.__db_name} exceeds the maximum length of 64 characters.')

        self.__client = MongoClient(self.mongo_server)
        self.__db = self.__client.get_database(self.__db_name)

    @property
    def db(self) -> Database:
        """Interface to Mongo database in pymongo driver."""
        return self.__db

    def create_ordered_object_id(self) -> ObjectId:
        result = ObjectId()

        retry_count = 0
        while result <= self.__prev_object_id:
            retry_count = retry_count + 1
            if retry_count == 0:
                self.context.log.warning('MongoDB generated ObjectId not in increasing order, retrying.')
                result = ObjectId()

        if retry_count != 0:
            self.context.log.warning(f'Generated ObjectId in increasing order after {retry_count} retries.')

        self.__prev_object_id = result
        return result

    def delete_db(self) -> None:
        """Permanently deletes (drops) the database with all records
        in it without the possibility to recover them later.

        This method should only be used to free storage. For
        all other purposes, methods that preserve history should
        be used.

        ATTENTION - THIS METHOD WILL DELETE ALL DATA WITHOUT
        THE POSSIBILITY OF RECOVERY. USE WITH CAUTION.
        """
        if self.read_only is not None and self.read_only:
            raise Exception(f'Attempting to drop (delete) database for the data source {self.data_source_name} '
                            f'where ReadOnly flag is set.')
        if self.__client is not None and self.__db is not None:
            if self.__env_type in [EnvType.Dev, EnvType.User, EnvType.Test]:
                self.__client.drop_database(self.__db)
            else:
                raise Exception(f'As an extra safety measure, database {self.__db_name} cannot be '
                                f'dropped because this operation is not permitted for database '
                                f'instance type {self.__env_type.name.upper()}.')
