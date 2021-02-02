# -*- coding: utf-8 -*-

from io import StringIO
from pathlib import Path

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .base import BaseFileParser


class PDFFileParser(BaseFileParser):
    """ Class for parsing and extracting text out of PDF files """

    extension = ".pdf"

    def __init__(self, encoding: str = "UTF-8"):
        """
        Initializes the PDF file parser internal attributes
        :param encoding: PDF files encoding
        """

        self._resource_manager = PDFResourceManager()
        self._layout_params = LAParams()

        self.string_buffer = StringIO()
        self.text_converter = TextConverter(
            rsrcmgr=self._resource_manager,
            laparams=self._layout_params,
            outfp=self.string_buffer,
            codec=encoding,
        )

    def _reset_buffer(self) -> int:
        """
        Resets the current string buffer so future reads do not accumulate
        :return: size of the string buffer
        """

        self.string_buffer.truncate(0)
        self.string_buffer.seek(0)
        return 0

    def _trim_string(self) -> str:
        """
        Trims the content of the string buffer by compacting paragraphs into lines
        :returns: trimmed text
        """

        text = self.string_buffer.getvalue()
        text = (line.replace("\n", " ") for line in text.split("\n\n"))
        return "\n".join(text)

    def check_extension(self, file_path: str) -> bool:
        """
        Checks for the .pdf file extension of the provided file.
        :param file_path: path to the target file
        :return: whether it has a valid extension
        """

        return Path(file_path).suffix == self.extension

    def extract_text(self, file_path: str) -> str:
        """
        Extracts plain text from a more extensible file type.
        :param file_path: path to the target file
        :return: plain text
        """

        if self.check_extension(file_path) is False:
            raise ValueError(f"Invalid extension: {file_path}")

        interpreter = PDFPageInterpreter(
            rsrcmgr=self._resource_manager,
            device=self.text_converter,
        )

        with open(file_path, mode="rb") as file:
            for page in PDFPage.get_pages(file):
                interpreter.process_page(page)

        t = self._trim_string()
        _ = self._reset_buffer()
        return t
