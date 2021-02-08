# -*- coding: utf-8 -*-

import json
from typing import Generator

from ..parsers import JSONFileParser
from ..parsers import PDFFileParser
from ..parsers import TextFileParser


class LocalJSONFile:
    """ Class containing the contents of a JSON file """

    def __init__(self, file_path: str, file_parser: JSONFileParser):
        """
        Initializes the object and parses the JSON contents
        :param file_path: path to the JSON file
        :param file_parser: parser for the JSON file
        """

        self.parser = file_parser
        self.content = file_parser.extract_text(file_path)
        self.struct = json.loads(self.content)

    def all_items(self) -> Generator:
        """
        Iterates over the top-level JSON array
        :return: deeper-level object
        """

        if type(self.struct) != list:
            raise ValueError("The JSON file must be a top-level array")

        for item in self.struct:
            yield item


class LocalPDFFile:
    """ Class containing the contents of a PDF file """

    def __init__(self, file_path: str, file_parser: PDFFileParser):
        """
        Initializes the object and parses the PDF contents
        :param file_path: path to the PDF file
        :param file_parser: parser for the PDF file
        """

        self.parser = file_parser
        self.content = file_parser.extract_text(file_path)

    def all_lines(self) -> str:
        """
        Iterates over the PDF content text lines
        :return: text line
        """

        for line in self.content.splitlines():
            yield line


class LocalTextFile:
    """ Class containing the contents of a TXT file """

    def __init__(self, file_path: str, file_parser: TextFileParser):
        """
        Initializes the object and parses the TXT contents
        :param file_path: path to the TXT file
        :param file_parser: parser for the TXT file
        """

        self.parser = file_parser
        self.content = file_parser.extract_text(file_path)

    def all_lines(self) -> str:
        """
        Iterates over the TXT content text lines
        :return: text line
        """

        for line in self.content.splitlines():
            yield line
