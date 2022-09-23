# -*- coding: utf-8 -*-

import logging

from json import JSONDecoder
from json import JSONDecodeError
from typing import AnyStr

from .base import BaseBinaryDecoder
from .base import BasePlainDecoder


logger = logging.getLogger()


class CustomJSONDecoder:
    """Custom JSON decoder class"""

    def __init__(self, **kwargs):
        """
        Initializes the JSON content decoder
        :param kwargs: keyword arguments for the default decoder
        """

        self._decoder = JSONDecoder(**kwargs)

    def _decode(self, data: str) -> object:
        """
        Decodes a JSON string into a Python object
        :param data: JSON data
        :return: Python object
        """

        try:
            obj = self._decoder.decode(data)
        except JSONDecodeError:
            logger.error(f"The provided data does not contains a valid JSON")
            logger.error(f"Data: {data}")
            raise

        return obj


class JSONBinaryDecoder(BaseBinaryDecoder, CustomJSONDecoder):
    """JSON binary contents decoder class"""

    def decode(self, data: bytes) -> object:
        """
        Decodes a JSON bytes into a Python object
        :param data: JSON as bytes
        :return: Python object
        """

        decoded_string = self._decode_string(data)
        decoded_json = super()._decode(decoded_string)

        return decoded_json


class JSONPlainDecoder(BasePlainDecoder, CustomJSONDecoder):
    """JSON plain contents decoder class"""

    def decode(self, data: str) -> object:
        """
        Decodes a JSON string into a Python object
        :param data: JSON as string
        :return: Python object
        """

        return super()._decode(data)
