# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseFileHandler(ABC):
    """Interface for the file handler classes"""

    @abstractmethod
    def read_file(self, file_path: str) -> Any:
        """
        Reads contents from a file at the provided path
        :param file_path: path to the readable file
        :return: content read
        """

        raise NotImplementedError()

    @abstractmethod
    def write_file(self, file_path: str, content: Any) -> None:
        """
        Writes contents to a file at the provided path
        :param file_path: path to the writable file
        :param content: content to write
        """

        raise NotImplementedError()
