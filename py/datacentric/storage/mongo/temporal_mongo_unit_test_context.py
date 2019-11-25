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
