# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class BaseFileParser(metaclass=ABCMeta):
    """ Interface for the file parser classes """

    @property
    @abstractmethod
    def extension(self):
        """ File extension for a particular parser """

        raise NotImplementedError()

    @abstractmethod
    def check_extension(self, file_path: str) -> bool:
        """
        Checks for the file extension of the provided file.
        :param file_path: path to the target file
        :return: whether it has a valid extension
        """

        raise NotImplementedError()

    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """
        Extracts plain text from a more extensible file type.
        :param file_path: path to the target file
        :return: plain text
        """

        raise NotImplementedError()
