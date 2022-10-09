# -*- coding: utf-8 -*-

from src.dialect_map_io.encoding import JSONBinaryDecoder
from src.dialect_map_io.encoding import JSONPlainDecoder


def test_json_binary_decoding():
    """Checks the correct parsing of bytes encoded JSONs"""

    json_decoder = JSONBinaryDecoder()

    json_bytes = b'{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_decoder.decode(json_bytes) == json_dict


def test_json_plain_decoding():
    """Checks the correct parsing of string encoded JSONs"""

    json_decoder = JSONPlainDecoder()

    json_str = '{"field_1": "example", "field_2": [1, 2, 3]}'
    json_dict = {"field_1": "example", "field_2": [1, 2, 3]}

    assert json_decoder.decode(json_str) == json_dict
