# -*- coding: utf-8 -*-

from .base import BaseBinaryEncoder
from .base import BasePlainEncoder


class TextBinaryEncoder(BaseBinaryEncoder):
    """Text binary contents encoder class"""

    def encode(self, data: object) -> bytes:
        """
        Encodes a string as bytes
        :param data: string
        :return: bytes
        """

        encoded_string = str(data)
        encoded_bytes = self._encode_string(encoded_string)

        return encoded_bytes


class TextPlainEncoder(BasePlainEncoder):
    """Text plain contents encoder class"""

    def encode(self, data: object) -> str:
        """
        Encodes a string as a string
        :param data: string
        :return: string
        """

        return str(data)
