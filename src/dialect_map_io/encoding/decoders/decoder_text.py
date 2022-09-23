# -*- coding: utf-8 -*-

from .base import BasePlainDecoder


class TextPlainDecoder(BasePlainDecoder):
    """Text plain contents decoder class"""

    def decode(self, data: str) -> str:
        """
        Decodes a string blob into a string
        :param data: string blob
        :return: string
        """

        return data
