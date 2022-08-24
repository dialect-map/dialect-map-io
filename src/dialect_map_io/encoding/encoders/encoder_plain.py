# -*- coding: utf-8 -*-

from json import JSONEncoder

from .base import BasePlainEncoder


class JSONPlainEncoder(BasePlainEncoder):
    """JSON contents encoder class"""

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


class TXTPlainEncoder(BasePlainEncoder):
    """TXT contents encoder class"""

    def encode(self, data: object) -> str:
        """
        Encodes a string as a string
        :param data: string
        :return: string
        """

        return str(data)
