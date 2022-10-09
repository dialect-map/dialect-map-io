# -*- coding: utf-8 -*-

import logging

from pathlib import Path

from .base import BaseFileHandler
from ...encoding import BaseBinaryDecoder
from ...encoding import BaseBinaryEncoder
from ...encoding import PDFBinaryDecoder
from ...encoding import PDFBinaryEncoder

logger = logging.getLogger()


class BinaryFileHandler(BaseFileHandler):
    """Class handling the contents of binary files"""

    def __init__(self, decoder: BaseBinaryDecoder, encoder: BaseBinaryEncoder):
        """
        Initializes the binary file handler
        :param decoder: decoder for reading content
        :param encoder: encoder for writing content
        """

        self.decoder = decoder
        self.encoder = encoder

    def read_file(self, file_path: str) -> object:
        """
        Reads contents from a file at the provided path
        :param file_path: path to the readable file
        :return: bytes read
        """

        with open(file_path, "rb") as file:
            contents = file.read()

        return self.decoder.decode(contents)

    def write_file(self, file_path: str, content: object) -> None:
        """
        Writes contents to a file at the provided path
        :param file_path: path to the writable file
        :param content: bytes to write
        """

        if Path(file_path).exists():
            logging.warning(f"File {file_path} already exists")
            return

        content = self.encoder.encode(content)

        with open(file_path, "wb") as file:
            file.write(content)


class PDFFileHandler(BinaryFileHandler):
    """Class handling the contents of PDF files"""

    def __init__(self):
        decoder = PDFBinaryDecoder()
        encoder = PDFBinaryEncoder()

        super().__init__(decoder, encoder)
