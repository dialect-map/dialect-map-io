# -*- coding: utf-8 -*-

from pathlib import Path


DATA_FOLDER = ".data"

FEED_FOLDER = Path(__file__).parent \
    .joinpath(DATA_FOLDER) \
    .joinpath("feed")

JSON_FOLDER = Path(__file__).parent \
    .joinpath(DATA_FOLDER) \
    .joinpath("json")

PDF_FOLDER = Path(__file__).parent \
    .joinpath(DATA_FOLDER) \
    .joinpath("pdf")

TXT_FOLDER = Path(__file__).parent \
    .joinpath(DATA_FOLDER) \
    .joinpath("txt")
