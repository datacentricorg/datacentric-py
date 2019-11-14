from datacentric.storage.context import Context
from datacentric.storage.mongo.temporal_mongo_data_source import TemporalMongoDataSource
from datacentric.storage.db_name import DbNameKey
from datacentric.storage.instance_type import EnvType


class TemporalTestContext:
    def __init__(self, test):
        self.test = test

    def __enter__(self):
        context = Context()

        source = TemporalMongoDataSource()
        db_name = DbNameKey()
        db_name.instance_type = EnvType.Test
        db_name.instance_name = self.test.id().split('.')[-2]
        db_name.env_name = self.test.id().split('.')[-1]
        source.db_name = db_name
        source.init(context)

        context.data_source = source
        context.data_set = context.data_source.create_common()

        return context

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit tests context')
