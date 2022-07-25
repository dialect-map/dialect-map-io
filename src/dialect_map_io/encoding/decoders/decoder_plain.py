# -*- coding: utf-8 -*-

import logging

from json import JSONDecoder
from json import JSONDecodeError
from typing import AnyStr

from .base import BasePlainDecoder


logger = logging.getLogger()


class JSONPlainDecoder(BasePlainDecoder):
    """JSON contents decoder class"""

    def __init__(self, **kwargs):
        """
        Initializes the JSON content decoder
        :param kwargs: keyword arguments for the default decoder
        """

        self._decoder = JSONDecoder(**kwargs)

    def decode(self, data: AnyStr) -> object:
        """
        Decodes a string/bytes blob into a Python object
        :param data: string/bytes blob
        :return: Python object
        """

        string = self._decode(data)

        try:
            obj = self._decoder.decode(string)
        except JSONDecodeError:
            logger.error(f"The provided data does not contains a valid JSON")
            logger.error(f"Data: {string}")
            raise

        return obj


class TXTPlainDecoder(BasePlainDecoder):
    """TXT contents decoder class"""

    def decode(self, data: AnyStr) -> str:
        """
        Decodes a string/bytes blob into a string
        :param data: string/bytes blob
        :return: string
        """

        return self._decode(data)
