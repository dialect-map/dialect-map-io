# -*- coding: utf-8 -*-

import pytest
from src.dialect_map_io.parsers import PDFTextParser

from ..__paths import PDF_FOLDER
from ..__paths import TXT_FOLDER


@pytest.fixture(scope="module")
def pdf_parser() -> PDFTextParser:
    """
    Creates a parser for the PDF files
    :return: parser
    """

    return PDFTextParser()


def test_pdf_parsing(pdf_parser: PDFTextParser):
    """
    Tests the correct text parsing from a PDF file
    :param pdf_parser: initialized parser
    """

    sample_pdf = PDF_FOLDER.joinpath("example_arxiv.pdf")
    sample_txt = TXT_FOLDER.joinpath("example_arxiv.txt")

    extracted_text = pdf_parser.parse_file(sample_pdf)
    original_text = open(sample_txt, "r").read()

    # Removing last new line character (\n)
    assert extracted_text == original_text[:-1]
