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
from typing import Union, Optional, List, Any
from abc import ABC, abstractmethod
from datacentric.storage.key import Key


class DataSetKey(Key):
    """
    Dataset is a concept similar to a folder, applied to data in any
    data source including relational or document databases, OData
    endpoints, etc.

    Datasets can be stored in other datasets. The dataset where dataset
    record is stored is called parent dataset.

    Dataset has an Imports array which provides the list of TemporalIds of
    datasets where records are looked up if they are not found in the
    current dataset. The specific lookup rules are specific to the data
    source type and described in detail in the data source documentation.

    Some data source types do not support Imports. If such data
    source is used with a dataset where Imports array is not empty,
    an error will be raised.

    The root dataset uses TemporalId.Empty and does not have versions
    or its own DataSet record. It is always last in the dataset
    lookup sequence. The root dataset cannot have Imports.
    """
    pass