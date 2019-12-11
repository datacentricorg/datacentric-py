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

from typing import Union, List
from datacentric.storage.key import Key

class KeyUtil:
    """
    Utilities for working with key strings.
    """

    @classmethod
    def remove_prefix(cls, key: Union[str, Key], key_type: str) -> str:
        """
        Parse key string in KeyType=A;B;C format, verify that the first part (KeyType)
        matches key_type argument, and return the second part (A;B;C).

        This method verifies that the second part does not contain =, but does not
        verify how many semicolon delimiters it has.
        """
        tokens: List[str] = key.split('=')
        if len(tokens) != 2:
            raise Exception(f'Key {key} contains more than one occurrence of =.')
        if tokens[0] != key_type:
            raise Exception(f'Key {key} does not start from {key_type}=.')
        return tokens[1]

    @classmethod
    def get_token(cls, key: Union[str, Key], key_type: str, token_count: int, token_index: int) -> str:
        """
        Parse key string in KeyType=A;B;C format, verify that the first part (KeyType)
        matches key_type argument and return semicolon delimited token at token_index
        from the second part.

        This method verifies that the second part does not contain = and how many semicolon
        delimiters it has.
        """
        second_part: str = cls.remove_prefix(key, key_type)
        tokens: List[str] = second_part.split(';')
        if len(tokens) != token_count:
            raise Exception(f'Key {key} must have exactly {token_count} semicolon delimited tokens after =.')
        return tokens[token_index]
