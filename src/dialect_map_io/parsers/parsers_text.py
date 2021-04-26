# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .__utils import check_extension


class BaseTextParser(ABC):
    """Interface for the text parser classes"""

    @property
    @abstractmethod
    def extension(self):
        """File extension for a particular parser"""

        raise NotImplementedError()

    @abstractmethod
    def parse_file(self, file_path: str) -> str:
        """
        Parses the provided text containing file
        :param file_path: path to the target file
        :return: decoded data
        """

        raise NotImplementedError()


class PDFTextParser(BaseTextParser):
    """Class for parsing and extracting text from PDF files"""

    extension = ".pdf"

    def __init__(self, encoding: str = "UTF-8"):
        """
        Initializes the PDF text parser internal attributes
        :param encoding: PDF files encoding
        """

        self._resource_manager = PDFResourceManager()
        self._layout_params = LAParams()

        self.file_encoding = encoding
        self.string_buffer = StringIO()
        self.text_converter = TextConverter(
            rsrcmgr=self._resource_manager,
            laparams=self._layout_params,
            outfp=self.string_buffer,
            codec=self.file_encoding,
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

    def parse_file(self, file_path: str) -> str:
        """
        Extracts text from the provided PDF file
        :param file_path: path to the target file
        :return: plain text
        """

        if check_extension(file_path, self.extension) is False:
            raise ValueError(f"Invalid file extension: {file_path}")

        interpreter = PDFPageInterpreter(
            rsrcmgr=self._resource_manager,
            device=self.text_converter,
        )

        with open(file=file_path, mode="rb") as file:
            for page in PDFPage.get_pages(file):
                interpreter.process_page(page)

        t = self._trim_string()
        _ = self._reset_buffer()
        return t


class TXTTextParser(BaseTextParser):
    """Class for parsing and extracting text from TXT files"""

    extension = ".txt"

    def parse_file(self, file_path: str) -> str:
        """
        Extracts text from the provided TXT file
        :param file_path: path to the target file
        :return: plain text
        """

        if check_extension(file_path, self.extension) is False:
            raise ValueError(f"Invalid file extension: {file_path}")

        with open(file=file_path, mode="r") as file:
            contents = file.read()

        return contents
