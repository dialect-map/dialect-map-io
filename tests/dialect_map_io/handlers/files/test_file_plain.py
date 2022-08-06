# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_io.handlers import JSONFileHandler

from ...__paths import JSON_FOLDER


@pytest.fixture(scope="module")
def json_file_handler() -> JSONFileHandler:
    """
    Creates a JSON file handler
    :return: JSON file handler
    """

    return JSONFileHandler()


def test_valid_json_file(json_file_handler: JSONFileHandler):
    """
    Tests the correct decoding and listing of a valid JSON file
    :param json_file_handler: JSON file handler
    """

    file_path = JSON_FOLDER.joinpath("example_data.json")
    file_path = str(file_path)

    contents = json_file_handler.read_file(file_path)
    assert isinstance(contents, list)

    for index, struct in enumerate(contents):
        number = index + 1

        assert struct["field_1"] == f"name {number}"
        assert struct["field_2"] == f"description {number}"
        assert struct["field_3"] == number


def test_invalid_json_file(json_file_handler: JSONFileHandler):
    """
    Tests the correct error raising of an invalid JSON file
    :param json_file_handler: JSON file handler
    """

    file_path = JSON_FOLDER.joinpath("example_error.json")
    file_path = str(file_path)

    assert pytest.raises(ValueError, json_file_handler.read_file, file_path)
