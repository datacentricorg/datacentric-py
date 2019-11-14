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

from typing import Optional
from abc import ABC
from datacentric.storage.typed_key import TypedKey
from datacentric.storage.root_record import RootRecord
from datacentric.storage.instance_type import EnvType


class DbNameKey(TypedKey['DbName']):
    """
    This class enforces strict naming conventions
    for database naming. While format of the resulting database
    name is specific to data store type, it always consists
    of three tokens: InstanceType, InstanceName, and EnvName.
    The meaning of InstanceName and EnvName tokens depends on
    the value of InstanceType enumeration.

    This record is stored in root dataset.
    """

    __slots__ = ('instance_type', 'instance_name', 'env_name')

    instance_type: EnvType
    instance_name: Optional[str]
    env_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.instance_type = None
        """
        Instance type enumeration.

        Some API functions are restricted based on the instance type.
        """

        self.instance_name = None
        """
        The meaning of instance name depends on the instance type.

        * For PROD, UAT, and DEV instance types, instance name
        identifies the endpoint.

        * For USER instance type, instance name is user alias.

        * For TEST instance type, instance name is the name of
        the unit test class (test fixture).
        """

        self.env_name = None
        """
        The meaning of environment name depends on the instance type.

        * For PROD, UAT, DEV, and USER instance types, it is the
        name of the user environment selected in the client.

        * For TEST instance type, it is the test method name.
        """


class DbName(RootRecord[DbNameKey], ABC):
    """
    This class enforces strict naming conventions
    for database naming. While format of the resulting database
    name is specific to data store type, it always consists
    of three tokens: InstanceType, InstanceName, and EnvName.
    The meaning of InstanceName and EnvName tokens depends on
    the value of InstanceType enumeration.

    This record is stored in root dataset.
    """

    __slots__ = ('instance_type', 'instance_name', 'env_name')

    instance_type: Optional[EnvType]
    instance_name: Optional[str]
    env_name: Optional[str]

    def __init__(self):
        super().__init__()

        self.instance_type = None
        """
        Instance type enumeration.

        Some API functions are restricted based on the instance type.
        """

        self.instance_name = None
        """
        The meaning of instance name depends on the instance type.

        * For PROD, UAT, and DEV instance types, instance name
        identifies the endpoint.

        * For USER instance type, instance name is user alias.

        * For TEST instance type, instance name is the name of
        the unit test class (test fixture).
        """

        self.env_name = None
        """
        The meaning of environment name depends on the instance type.

        * For PROD, UAT, DEV, and USER instance types, it is the
        name of the user environment selected in the client.

        * For TEST instance type, it is the test method name.
        """
