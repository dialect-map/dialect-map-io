# -*- coding: utf-8 -*-

from json import JSONEncoder

from .base import BaseBinaryEncoder
from .base import BasePlainEncoder


class JSONBinaryEncoder(BaseBinaryEncoder):
    """JSON binary contents encoder class"""

    def __init__(self, **kwargs):
        """
        Initializes the JSON content encoder
        :param kwargs: keyword arguments for the default encoder
        """

        self._encoder = JSONEncoder(**kwargs, ensure_ascii=False)

    def encode(self, data: object) -> bytes:
        """
        Encodes a Python object as a string
        :param data: Python object
        :return: encoded bytes
        """

        encoded_string = self._encoder.encode(data)
        encoded_bytes = self._encode_string(encoded_string)

        return encoded_bytes


class JSONPlainEncoder(BasePlainEncoder):
    """JSON plain contents encoder class"""

    def __init__(self, **kwargs):
        """
        Initializes the JSON content encoder
        :param kwargs: keyword arguments for the default encoder
        """

        self._encoder = JSONEncoder(**kwargs, ensure_ascii=False)

    def encode(self, data: object) -> str:
        """
        Encodes a Python object as a string
        :param data: Python object
        :return: encoded string
        """

        return self._encoder.encode(data)
