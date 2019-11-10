from abc import ABC
from typing import TypeVar
from bson import ObjectId

from datacentric.storage.context import Context
from datacentric.storage.typed_record import TypedRecord

TKey = TypeVar('TKey')


class RootRecord(TypedRecord[TKey], ABC):
    """
    Base class of records stored in root dataset of the data store.

    init(...) method of this class sets data_set to temporal_id.empty.
    """

    __slots__ = ()

    def __init__(self):
        super().__init__()

    def init(self, context: Context) -> None:
        """
        Set Context property and perform validation of the record's data,
        then initialize any fields or properties that depend on that data.

        This method must work when called multiple times for the same instance,
        possibly with a different context parameter for each subsequent call.

        All overrides of this method must call base.Init(context) first, then
        execute the rest of the code in the override.
        """

        # Initialize base before executing the rest of the code in this method
        super().init(context)

        # For this base type of records stored in root dataset,
        # set data_set element to the value designated for the
        # root dataset: temporal_id.empty.
        self.data_set = ObjectId('000000000000000000000000')
