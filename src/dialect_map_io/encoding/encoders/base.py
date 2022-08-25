# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic

from ..base import BaseBinaryContent
from ..base import BasePlainContent


class BaseEncoder(ABC):
    """Interface for the encoder classes"""

    @abstractmethod
    def encode(self, data: Any) -> Any:
        """
        Encodes a Python object as a string/bytes blob
        :param data: Python object
        :return: string/bytes blob
        """

        raise NotImplementedError()


class BaseBinaryEncoder(BaseEncoder, Generic[BaseBinaryContent]):
    """Interface for the binary encoder classes"""

    @abstractmethod
    def encode(self, data: BaseBinaryContent) -> bytes:
        """
        Encodes a Python object as a bytes blob
        :param data: Python object
        :return: bytes blob
        """

        raise NotImplementedError()


class BasePlainEncoder(BaseEncoder, Generic[BasePlainContent]):
    """Interface for the plain encoder classes"""

    @abstractmethod
    def encode(self, data: BasePlainContent) -> str:
        """
        Encodes a Python object as a string blob
        :param data: Python object
        :return: string blob
        """

        raise NotImplementedError()
