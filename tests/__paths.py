# -*- coding: utf-8 -*-

from pathlib import Path


PROJECT_PATH = Path(__file__).parent

DATA_FOLDER = PROJECT_PATH.joinpath(".data")
META_FOLDER = PROJECT_PATH.joinpath(".metadata")

# Samples of what is considered 'data'
DATA_JSON_FOLDER = DATA_FOLDER.joinpath("json")
DATA_PDF_FOLDER = DATA_FOLDER.joinpath("pdf")
DATA_TXT_FOLDER = DATA_FOLDER.joinpath("txt")

# Samples of what is considered 'metadata'
META_FEED_FOLDER = META_FOLDER.joinpath("feed")
META_JSON_FOLDER = META_FOLDER.joinpath("json")
