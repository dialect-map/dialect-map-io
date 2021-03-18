# -*- coding: utf-8 -*-

from pathlib import Path


def check_extension(file_path: str, extension: str) -> bool:
    """
    Checks for the file extension of the provided file
    :param file_path: path to the target file
    :param extension: extension to check against
    :return: whether it has a valid extension
    """

    return Path(file_path).suffix == extension
