# -*- coding: utf-8 -*-

import pytest
from src.parsers import PDFFileParser

from ..__paths import PDF_FOLDER
from ..__paths import TXT_FOLDER


@pytest.fixture(scope="module")
def pdf_parser() -> PDFFileParser:
    """
    Creates a parser for the PDF files
    :return: parser
    """

    return PDFFileParser()


def test_check_extension(pdf_parser: PDFFileParser):
    """
    Tests the correct checking of a PDF file extension
    :param pdf_parser: initialized parser
    """

    sample_pdf = PDF_FOLDER.joinpath("example_arxiv.pdf")
    assert pdf_parser.check_extension(sample_pdf)


def test_text_extract(pdf_parser: PDFFileParser):
    """
    Tests the correct text extraction from a PDF file
    :param pdf_parser: initialized parser
    """

    sample_pdf = PDF_FOLDER.joinpath("example_arxiv.pdf")
    sample_txt = TXT_FOLDER.joinpath("example_arxiv.txt")

    extracted_text = pdf_parser.extract_text(sample_pdf)
    original_text = open(sample_txt, "r").read()

    # Removing last new line character (\n)
    assert extracted_text == original_text[:-1]
