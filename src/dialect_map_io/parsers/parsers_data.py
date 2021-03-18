# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from json import JSONDecoder
from typing import Any

from .__utils import check_extension


class BaseDataParser(ABC):
    """ Interface for the data parser classes """

    @property
    @abstractmethod
    def extension(self):
        """ File extension for a particular parser """

        raise NotImplementedError()

    @abstractmethod
    def parse_file(self, file_path: str) -> Any:
        """
        Parses the provided data containing file
        :param file_path: path to the target file
        :return: decoded data
        """

        raise NotImplementedError()

    @abstractmethod
    def parse_bytes(self, encoded_str: bytes) -> Any:
        """
        Parses the provided bytes encoded JSON
        :param encoded_str: bytes encoded JSON
        :return: decoded data
        """

        raise NotImplementedError()

    @abstractmethod
    def parse_str(self, encoded_str: str) -> Any:
        """
        Parses the provided string encoded data
        :param encoded_str: string encoded data
        :return: decoded data
        """

        raise NotImplementedError()


class JSONDataParser(BaseDataParser):
    """
    Class for parsing and extracting JSON data

    For Python 3.8+, combine both 'parse_bytes' and 'parse_str'
    methods into a single one using @singledispatchmethod
    Ref: https://docs.python.org/3/library/functools.html
    """

    extension = ".json"

    def __init__(self, **decoder_args):
        """
        Initializes the JSON parser
        :param decoder_args: keyword arguments for the JSONDecoder
        """

        self.decoder = JSONDecoder(**decoder_args)

    def parse_file(self, file_path: str) -> Any:
        """
        Parses the provided JSON data file
        :param file_path: path to the target file
        :return: decoded data
        """

        if check_extension(file_path, self.extension) is False:
            raise ValueError(f"Invalid file extension: {file_path}")

        with open(file=file_path, mode="r") as file:
            contents = file.read()

        return self.decoder.decode(contents)

    def parse_bytes(self, encoded_str: bytes) -> Any:
        """
        Parses the provided bytes encoded JSON
        :param encoded_str: bytes encoded JSON
        :return: decoded data
        """

        string = encoded_str.decode("UTF-8")
        return self.decoder.decode(string)

    def parse_str(self, encoded_str: str) -> Any:
        """
        Parses the provided string encoded JSON
        :param encoded_str: string encoded JSON
        :return: decoded data
        """

        return self.decoder.decode(encoded_str)
