# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from json import JSONDecoder
from typing import AnyStr

from .__utils import check_extension


class BaseDataParser(ABC):
    """Interface for the data parser classes"""

    @property
    @abstractmethod
    def extension(self):
        """File extension for a particular parser"""

        raise NotImplementedError()

    @abstractmethod
    def parse_file(self, file_path: str) -> object:
        """
        Parses the provided data containing file
        :param file_path: path to the target file
        :return: decoded data
        """

        raise NotImplementedError()

    @abstractmethod
    def parse_string(self, encoded_data: AnyStr) -> object:
        """
        Parses the provided string encoded data
        :param encoded_data: string encoded data
        :return: decoded data
        """

        raise NotImplementedError()


class JSONDataParser(BaseDataParser):
    """Class for parsing and extracting JSON data"""

    extension = ".json"

    def __init__(self, **decoder_args):
        """
        Initializes the JSON parser
        :param decoder_args: keyword arguments for the JSONDecoder
        """

        self.decoder = JSONDecoder(**decoder_args)

    def parse_file(self, file_path: str) -> object:
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

    def parse_string(self, encoded_data: AnyStr) -> object:
        """
        Parses the provided string encoded JSON
        :param encoded_data: string encoded JSON
        :return: decoded data
        """

        if isinstance(encoded_data, bytes):
            string = encoded_data.decode("UTF-8")
        elif isinstance(encoded_data, str):
            string = encoded_data
        else:
            raise TypeError("Encoded data must be either 'bytes' or 'str'")

        return self.decoder.decode(string)
