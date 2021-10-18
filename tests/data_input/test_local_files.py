# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_io.data_input import LocalDataFile
from src.dialect_map_io.parsers import JSONDataParser

from ..__paths import DATA_JSON_FOLDER


@pytest.fixture(scope="module")
def json_array_input() -> LocalDataFile:
    """
    Creates a local JSON file input source
    :return: data file input source
    """

    file_path = DATA_JSON_FOLDER.joinpath("example_data.json")
    file_path = str(file_path)
    data_parser = JSONDataParser()

    return LocalDataFile(file_path, data_parser)


@pytest.fixture(scope="module")
def json_object_input() -> LocalDataFile:
    """
    Creates a local JSON file input source
    :return: data file input source
    """

    file_path = DATA_JSON_FOLDER.joinpath("example_error.json")
    file_path = str(file_path)
    data_parser = JSONDataParser()

    return LocalDataFile(file_path, data_parser)


def test_json_file_all_items(json_array_input: LocalDataFile):
    """
    Tests the correct decoding and listing of a JSON-array file
    :param json_array_input: JSON file input
    """

    for index, struct in enumerate(json_array_input.iter_items()):
        number = index + 1

        assert struct["field_1"] == f"name {number}"
        assert struct["field_2"] == f"description {number}"
        assert struct["field_3"] == number


def test_json_file_error(json_object_input: LocalDataFile):
    """
    Tests the correct error raising of a non JSON-array file
    :param json_object_input: JSON file input
    """

    assert pytest.raises(ValueError, next, json_object_input.iter_items())
