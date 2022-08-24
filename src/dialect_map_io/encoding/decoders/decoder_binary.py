# -*- coding: utf-8 -*-

from io import BytesIO
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .base import BaseBinaryDecoder


class PDFBinaryDecoder(BaseBinaryDecoder[str]):
    """PDF contents decoder class"""

    def __init__(self, encoding: str = "UTF-8"):
        """
        Initializes the PDF content decoder
        :param encoding: PDF content encoding
        """

        self._buffer = StringIO()
        self._encoding = encoding
        self._layout_params = LAParams()
        self._resource_manager = PDFResourceManager()

        self._text_converter = TextConverter(
            rsrcmgr=self._resource_manager,
            laparams=self._layout_params,
            outfp=self._buffer,
            codec=self._encoding,
        )

    def _reset_buffer(self) -> int:
        """
        Resets the current string buffer so future reads do not accumulate
        :return: size of the string buffer
        """

        self._buffer.truncate(0)
        self._buffer.seek(0)
        return 0

    def _trim_string(self) -> str:
        """
        Trims the content of the string buffer by compacting paragraphs into lines
        :returns: trimmed text
        """

        text = self._buffer.getvalue()
        text = (line.replace("\n", " ") for line in text.split("\n\n"))
        return "\n".join(text)

    def decode(self, data: bytes) -> str:
        """
        Decodes a bytes stream into a string
        :param data: bytes stream
        :return: string
        """

        data_stream = BytesIO(data)
        interpreter = PDFPageInterpreter(
            rsrcmgr=self._resource_manager,
            device=self._text_converter,
        )

        for page in PDFPage.get_pages(data_stream):
            interpreter.process_page(page)

        t = self._trim_string()
        _ = self._reset_buffer()
        return t
