# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_io.parsers import JSONDataParser


@pytest.fixture(scope="module")
def json_parser() -> JSONDataParser:
    """
    Creates a parser for the JSON files
    :return: parser
    """

    return JSONDataParser()


def test_json_bytes_parsing(json_parser: JSONDataParser):
    """
    Checks the correct parsing of bytes encoded JSONs
    :param json_parser: initialized parser
    """

    json_bytes = b'{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_parser.parse_string(json_bytes) == json_dict


def test_json_string_parsing(json_parser: JSONDataParser):
    """
    Checks the correct parsing of string encoded JSONs
    :param json_parser: initialized parser
    """

    json_str = '{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_parser.parse_string(json_str) == json_dict
