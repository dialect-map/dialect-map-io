# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseEncoder(ABC):
    """Interface for the encoder classes"""

    @abstractmethod
    def encode(self, data: object) -> Any:
        """
        Encodes a Python object as a string/bytes blob
        :param data: Python object
        :return: string/bytes blob
        """

        raise NotImplementedError()


class BaseBinaryEncoder(BaseEncoder):
    """Interface for the binary encoder classes"""

    @staticmethod
    def _encode_string(data: object) -> bytes:
        """
        Encodes a string/bytes blob into as bytes
        :param data: string/bytes blob
        :return: bytes
        """

        if isinstance(data, bytes):
            raw_bytes = data
        elif isinstance(data, str):
            raw_bytes = data.encode("UTF-8")
        else:
            raise TypeError("Data must be of type 'bytes' or 'str'")

        return raw_bytes

    @abstractmethod
    def encode(self, data: object) -> bytes:
        """
        Encodes a Python object as a bytes blob
        :param data: Python object
        :return: bytes blob
        """

        raise NotImplementedError()


class BasePlainEncoder(BaseEncoder):
    """Interface for the plain encoder classes"""

    @abstractmethod
    def encode(self, data: object) -> str:
        """
        Encodes a Python object as a string blob
        :param data: Python object
        :return: string blob
        """

        raise NotImplementedError()
