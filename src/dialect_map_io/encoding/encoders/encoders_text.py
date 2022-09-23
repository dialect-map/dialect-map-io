# -*- coding: utf-8 -*-

from .base import BasePlainEncoder


class TextPlainEncoder(BasePlainEncoder):
    """Text plain contents encoder class"""

    def encode(self, data: object) -> str:
        """
        Encodes a string as a string
        :param data: string
        :return: string
        """

        return str(data)
