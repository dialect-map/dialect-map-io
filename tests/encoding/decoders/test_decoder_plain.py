# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_io.encoding import JSONPlainDecoder


@pytest.fixture(scope="module")
def json_decoder() -> JSONPlainDecoder:
    """
    Creates a decoder for the JSON contents
    :return: decoder
    """

    return JSONPlainDecoder()


def test_json_bytes_parsing(json_decoder: JSONPlainDecoder):
    """
    Checks the correct parsing of bytes encoded JSONs
    :param json_decoder: initialized parser
    """

    json_bytes = b'{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_decoder.decode(json_bytes) == json_dict


def test_json_string_parsing(json_decoder: JSONPlainDecoder):
    """
    Checks the correct parsing of string encoded JSONs
    :param json_decoder: initialized parser
    """

    json_str = '{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_decoder.decode(json_str) == json_dict
