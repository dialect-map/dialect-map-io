# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import AnyStr
from typing import Generic

from ..base import BaseBinaryContent
from ..base import BasePlainContent


class BaseDecoder(ABC):
    """Interface for the decoder classes"""

    @staticmethod
    def _decode_string(data: AnyStr) -> str:
        """
        Decodes a string/bytes blob into a string
        :param data: string/bytes blob
        :return: string
        """

        if isinstance(data, bytes):
            string = data.decode("UTF-8")
        elif isinstance(data, str):
            string = data
        else:
            raise TypeError("Data must be of type 'bytes' or 'str'")

        return string

    @abstractmethod
    def decode(self, data: Any) -> Any:
        """
        Decodes a string/bytes blob into a Python object
        :param data: string/bytes blob
        :return: Python object
        """

        raise NotImplementedError()


class BaseBinaryDecoder(BaseDecoder, Generic[BaseBinaryContent]):
    """Interface for the binary decoder classes"""

    @abstractmethod
    def decode(self, data: bytes) -> BaseBinaryContent:
        """
        Decodes a bytes blob into a Python object
        :param data: bytes blob
        :return: Python object
        """

        raise NotImplementedError()


class BasePlainDecoder(BaseDecoder, Generic[BasePlainContent]):
    """Interface for the plain decoder classes"""

    @abstractmethod
    def decode(self, data: AnyStr) -> BasePlainContent:
        """
        Decodes a string/bytes blob into a Python object
        :param data: string/bytes blob
        :return: Python object
        """

        raise NotImplementedError()
