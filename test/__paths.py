# -*- coding: utf-8 -*-

from pathlib import Path


PROJECT_PATH = Path(__file__).parent

DATA_FOLDER = PROJECT_PATH.joinpath(".data")

FEED_FOLDER = DATA_FOLDER.joinpath("feed")
JSON_FOLDER = DATA_FOLDER.joinpath("json")
PDF_FOLDER = DATA_FOLDER.joinpath("pdf")
TXT_FOLDER = DATA_FOLDER.joinpath("txt")
