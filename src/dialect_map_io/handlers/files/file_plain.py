# -*- coding: utf-8 -*-

import logging

from pathlib import Path
from typing import Generator

from .base import BaseFileHandler
from ...encoding import BasePlainDecoder
from ...encoding import BasePlainEncoder
from ...encoding import JSONPlainDecoder
from ...encoding import JSONPlainEncoder
from ...encoding import TextPlainDecoder
from ...encoding import TextPlainEncoder

logger = logging.getLogger()


class PlainFileHandler(BaseFileHandler):
    """Class handling the contents of plain files"""

    def __init__(self, decoder: BasePlainDecoder, encoder: BasePlainEncoder):
        """
        Initializes the plain file handler
        :param decoder: decoder for reading content
        :param encoder: encoder for writing content
        """

        self.decoder = decoder
        self.encoder = encoder

    def read_items(self, file_path: str) -> Generator:
        """
        Returns a generator over the content items
        :param file_path: path to the readable file
        :return: generator
        """

        contents = self.read_file(file_path)

        if isinstance(contents, str):
            yield from contents.splitlines()
        elif isinstance(contents, dict):
            yield from contents.items()
        elif isinstance(contents, list):
            yield from contents

        raise ValueError("File content is not iterable")

    def read_file(self, file_path: str) -> object:
        """
        Reads contents from a file at the provided path
        :param file_path: path to the readable file
        :return: content read
        """

        with open(file_path, "r") as file:
            contents = file.read()

        return self.decoder.decode(contents)

    def write_file(self, file_path: str, content: object) -> None:
        """
        Writes contents to a file at the provided path
        :param file_path: path to the writable file
        :param content: content to write
        """

        if Path(file_path).exists():
            logging.warning(f"File {file_path} already exists")
            return

        content = self.encoder.encode(content)

        with open(file_path, "w") as file:
            file.write(content)


class JSONFileHandler(PlainFileHandler):
    """Class handling the contents of JSON files"""

    def __init__(self):
        decoder = JSONPlainDecoder()
        encoder = JSONPlainEncoder()

        super().__init__(decoder, encoder)


class TextFileHandler(PlainFileHandler):
    """Class handling the contents of text files"""

    def __init__(self):
        decoder = TextPlainDecoder()
        encoder = TextPlainEncoder()

        super().__init__(decoder, encoder)
