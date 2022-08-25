# -*- coding: utf-8 -*-

from .base import BaseBinaryEncoder


class PDFBinaryEncoder(BaseBinaryEncoder[object]):
    """PDF contents encoder class"""

    def encode(self, data: object) -> bytes:
        """
        Encodes a string into a PDF bytes blob
        :param data: string to encode
        :return: bytes blob
        """

        raise NotImplementedError()
