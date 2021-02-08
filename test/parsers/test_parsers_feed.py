# -*- coding: utf-8 -*-

import pytest
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone

from src.models import ArxivFeedHeader
from src.models import ArxivFeedEntry
from src.models import ArxivFeedEntryAuthor
from src.models import ArxivFeedEntryLink
from src.parsers import ArxivFeedParser

from ..__paths import FEED_FOLDER


@pytest.fixture(scope="module")
def arxiv_header() -> ArxivFeedHeader:
    """
    Feed header object parsed from a sample Arxiv Atom feed
    :return: feed header object
    """

    feed_parser = ArxivFeedParser()

    feed_file = FEED_FOLDER.joinpath("arxiv_feed.xml")
    feed_text = open(feed_file, "r").read()
    feed_head = feed_parser.parse_header(feed_text)

    return feed_head


@pytest.fixture(scope="module")
def arxiv_entry() -> ArxivFeedEntry:
    """
    Feed entry object parsed from a sample Arxiv Atom feed
    :return: feed entry object
    """

    feed_parser = ArxivFeedParser()

    feed_file = FEED_FOLDER.joinpath("arxiv_feed.xml")
    feed_text = open(feed_file, "r").read()
    feed_objs = feed_parser.parse_entries(feed_text)

    return feed_objs[0]


def test_arxiv_header_parse(arxiv_header: ArxivFeedHeader):
    """
    Tests the correct parsing of the Arxiv feed headers fields
    :param feed_header: feed header object
    """

    assert arxiv_header.query_id == "http://arxiv.org/api/cHxbiOdZaP56ODnBPIenZhzg5f8"
    assert arxiv_header.query_url == (
        "http://arxiv.org/api/query?search_query=all:electron"
        "&id_list="
        "&start=0"
        "&max_results=1"
    )

    assert arxiv_header.results_ts == datetime.combine(
        date=date(2007, 10, 8),
        time=time(00, 00, 00),
        tzinfo=timezone(timedelta(hours=-4)),
    )


def test_arxiv_entries_parse(arxiv_entry: ArxivFeedEntry):
    """
    Tests the correct parsing of the Arxiv feed entries fields
    :param arxiv_entry: feed entry object
    """

    assert arxiv_entry.paper_id == "hep-ex/0307015"
    assert arxiv_entry.paper_rev == "1"
    assert arxiv_entry.paper_category == "hep-ex"
    assert arxiv_entry.paper_title == (
        "Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA"
    )

    assert arxiv_entry.paper_description == (
        "Multi-electron production is studied at high electron transverse momentum in "
        "positron- and electron-proton collisions using the H1 detector at HERA. The "
        "data correspond to an integrated luminosity of 115 pb-1. Di-electron and "
        "tri-electron event yields are measured."
    )

    assert arxiv_entry.paper_created_at == datetime.combine(
        date=date(2003, 7, 7),
        time=time(13, 46, 40),
        tzinfo=timezone(timedelta(hours=-4)),
    )

    assert arxiv_entry.paper_updated_at == datetime.combine(
        date=date(2003, 7, 8),
        time=time(13, 46, 40),
        tzinfo=timezone(timedelta(hours=-4)),
    )


def test_arxiv_entries_authors_parse(arxiv_entry: ArxivFeedEntry):
    """
    Tests the correct parsing of the Arxiv feed authors field
    :param arxiv_entry: feed entry object
    """

    assert arxiv_entry.paper_authors == [
        ArxivFeedEntryAuthor("H1 Collaboration"),
    ]


def test_arxiv_entries_links_parse(arxiv_entry: ArxivFeedEntry):
    """
    Tests the correct parsing of the Arxiv feed link fields
    :param arxiv_entry: feed entry object
    """

    assert arxiv_entry.paper_links == [
        ArxivFeedEntryLink("http://arxiv.org/abs/hep-ex/0307015v1", "text/html"),
        ArxivFeedEntryLink("http://arxiv.org/pdf/hep-ex/0307015v1", "application/pdf"),
    ]
