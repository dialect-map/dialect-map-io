# -*- coding: utf-8 -*-

import json

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseFileWriter(ABC):
    """ Interface for the data-output file writer classes """

    @abstractmethod
    def write_file(self, file_path: str, content: Any) -> None:
        """
        Writes into the provided content into the target file
        :param file_path: path to the writable file
        :param content: Python object to write
        """

        raise NotImplementedError()


class JSONFileWriter(BaseFileWriter):
    """ Class to write JSON-style content in a local file """

    def __init__(self, encoding: str = "UTF-8", **json_kwargs):
        """
        Initializes the JSON-style file writer
        :param encoding: JSON file desired encoding (optional)
        :param json_kwargs: key-word arguments for the JSON dump
        """

        if encoding != "ASCII":
            json_kwargs["ensure_ascii"] = False

        self.file_encoding = encoding
        self.json_kwargs = json_kwargs

    def write_file(self, file_path: str, content: Any) -> None:
        """
        Writes into the provided content string into the target file
        :param file_path: path to the writable file
        :param content: Python object to write
        """

        with open(file_path, "w", encoding=self.file_encoding) as file:
            json.dump(content, file, **self.json_kwargs)


class TextFileWriter(BaseFileWriter):
    """ Class to write text content in a local file """

    def __init__(self, encoding: str = "UTF-8"):
        """
        Initializes the text file writer
        :param encoding: file desired encoding (optional)
        """

        self.file_encoding = encoding

    def write_file(self, file_path: str, content: str) -> None:
        """
        Writes into the provided content string into the target file
        :param file_path: path to the writable file
        :param content: text to write
        """

        with open(file_path, "w", encoding=self.file_encoding) as file:
            file.write(content)
