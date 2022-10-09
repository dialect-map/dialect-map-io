# -*- coding: utf-8 -*-

from .base import BaseBinaryDecoder
from .base import BasePlainDecoder


class TextBinaryDecoder(BaseBinaryDecoder):
    """Text binary contents decoder class"""

    def decode(self, data: bytes) -> str:
        """
        Decodes a bytes blob into a string
        :param data: bytes blob
        :return: string
        """

        return self._decode_string(data)


class TextPlainDecoder(BasePlainDecoder):
    """Text plain contents decoder class"""

    def decode(self, data: str) -> str:
        """
        Decodes a string blob into a string
        :param data: string blob
        :return: string
        """

        return data
