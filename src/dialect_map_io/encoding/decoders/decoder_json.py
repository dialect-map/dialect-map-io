# -*- coding: utf-8 -*-

import logging

from json import JSONDecoder
from json import JSONDecodeError

from .base import BasePlainDecoder


logger = logging.getLogger()


class JSONPlainDecoder(BasePlainDecoder):
    """JSON plain contents decoder class"""

    def __init__(self, **kwargs):
        """
        Initializes the JSON content decoder
        :param kwargs: keyword arguments for the default decoder
        """

        self._decoder = JSONDecoder(**kwargs)

    def decode(self, data: str) -> object:
        """
        Decodes a string blob into a Python object
        :param data: string blob
        :return: Python object
        """

        try:
            obj = self._decoder.decode(data)
        except JSONDecodeError:
            logger.error(f"The provided data does not contains a valid JSON")
            logger.error(f"Data: {data}")
            raise

        return obj
