# -*- coding: utf-8 -*-

from .parsers_data import BaseDataParser
from .parsers_data import JSONDataParser

from .parsers_feed import BaseFeedParser
from .parsers_feed import ArxivFeedParser

from .parsers_file import BaseFileParser
from .parsers_file import JSONFileParser
from .parsers_file import PDFFileParser
from .parsers_file import TextFileParser

from .parsers_text import BaseTextParser
from .parsers_text import PDFTextParser
from .parsers_text import TXTTextParser
