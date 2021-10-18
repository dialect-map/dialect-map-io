# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ArxivFeedHeader:
    """
    Object containing the header fields of an Arxiv feed response

    :attr query_id: unique identifier assigned to the feed query
    :attr query_url: request URL assigned to the feed query
    :attr results_ts: timestamp of the last query results update
    """

    query_id: str
    query_url: str
    results_ts: datetime
