# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_io.encoding import PDFBinaryDecoder

from ...__paths import PDF_FOLDER
from ...__paths import TXT_FOLDER


@pytest.fixture(scope="module")
def pdf_decoder() -> PDFBinaryDecoder:
    """
    Creates a decoder for the PDF contents
    :return: decoder
    """

    return PDFBinaryDecoder()


def test_pdf_parsing(pdf_decoder: PDFBinaryDecoder):
    """
    Tests the correct decoding of a PDF binary contents
    :param pdf_decoder: initialized decoder
    """

    sample_pdf = PDF_FOLDER.joinpath("example_arxiv.pdf")
    sample_txt = TXT_FOLDER.joinpath("example_arxiv.txt")

    binary_text = open(sample_pdf, "rb").read()
    plain_text = open(sample_txt, "r").read()

    extracted_text = pdf_decoder.decode(binary_text)

    # Removing last new line character (\n)
    assert extracted_text == plain_text[:-1]
