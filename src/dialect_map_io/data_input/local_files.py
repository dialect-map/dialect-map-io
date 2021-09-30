# -*- coding: utf-8 -*-

from typing import Generator

from ..parsers import BaseDataParser
from ..parsers import BaseTextParser


class LocalDataFile:
    """Class containing the contents of a data file"""

    def __init__(self, file_path: str, data_parser: BaseDataParser):
        """
        Initializes the object and parses the file contents
        :param file_path: path to the data file
        :param data_parser: parser for the data file
        """

        self.parser = data_parser
        self.content = data_parser.parse_file(file_path)

    def iter_items(self) -> Generator:
        """
        Iterates over the top-level data structure
        :return: deeper-level object
        """

        if not isinstance(self.content, list):
            raise ValueError("The data file must be a top-level array")

        for item in self.content:
            yield item


class LocalTextFile:
    """Class containing the contents of a text file"""

    def __init__(self, file_path: str, text_parser: BaseTextParser):
        """
        Initializes the object and parses the file contents
        :param file_path: path to the text file
        :param text_parser: parser for the text file
        """

        self.parser = text_parser
        self.content = text_parser.parse_file(file_path)

    def iter_lines(self) -> Generator:
        """
        Iterates over the text lines
        :return: text line
        """

        for line in self.content.splitlines():
            yield line
