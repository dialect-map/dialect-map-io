# -*- coding: utf-8 -*-

import pytest
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone

from src.dialect_map_io.models import ArxivFeedHeader
from src.dialect_map_io.models import ArxivMetadata
from src.dialect_map_io.models import ArxivMetadataAuthor
from src.dialect_map_io.models import ArxivMetadataLink
from src.dialect_map_io.parsers import FeedMetadataParser

from ...__paths import META_FEED_FOLDER


@pytest.fixture(scope="module")
def feed_header() -> ArxivFeedHeader:
    """
    Feed header object parsed from a sample Arxiv Atom feed
    :return: feed header object
    """

    feed_parser = FeedMetadataParser()

    feed_file = META_FEED_FOLDER.joinpath("arxiv_feed.xml")
    feed_text = open(feed_file, "r").read()
    feed_head = feed_parser.parse_header(feed_text)

    return feed_head


@pytest.fixture(scope="module")
def feed_entry() -> ArxivMetadata:
    """
    Feed entry object parsed from a sample Arxiv Atom feed
    :return: feed entry object
    """

    feed_parser = FeedMetadataParser()

    feed_file = META_FEED_FOLDER.joinpath("arxiv_feed.xml")
    feed_text = open(feed_file, "r").read()
    feed_objs = feed_parser.parse_body(feed_text)

    return feed_objs[0]


def test_arxiv_header_parse(feed_header: ArxivFeedHeader):
    """
    Tests the correct parsing of the Arxiv feed headers fields
    :param feed_header: feed header object
    """

    assert feed_header.query_id == "http://arxiv.org/api/vBQMi2rCJvODLLmHWAdImdorN/8"
    assert feed_header.query_url == (
        "http://arxiv.org/api/query?search_query="
        "&id_list=hep-ex/0307015"
        "&start=0"
        "&max_results=10"
    )

    assert feed_header.results_ts == datetime.combine(
        date=date(2021, 3, 25),
        time=time(00, 00, 00),
        tzinfo=timezone(timedelta(hours=-4)),
    )


def test_arxiv_entries_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed entries fields
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_id == "hep-ex/0307015"
    assert feed_entry.paper_rev == "v1"
    assert feed_entry.paper_doi == "10.1140/epjc/s2003-01326-x"
    assert feed_entry.paper_category == "hep-ex"
    assert feed_entry.paper_title == (
        "Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA"
    )

    assert feed_entry.paper_description == (
        "Multi-electron production is studied at high electron transverse momentum in "
        "positron- and electron-proton collisions using the H1 detector at HERA. The "
        "data correspond to an integrated luminosity of 115 pb-1. Di-electron and "
        "tri-electron event yields are measured."
    )

    assert feed_entry.paper_created_at == datetime.combine(
        date=date(2003, 7, 7),
        time=time(17, 46, 40),
        tzinfo=timezone.utc,
    )

    assert feed_entry.paper_updated_at == datetime.combine(
        date=date(2003, 7, 7),
        time=time(17, 46, 40),
        tzinfo=timezone.utc,
    )


def test_arxiv_entries_authors_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed authors field
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_authors == [
        ArxivMetadataAuthor("H1 Collaboration"),
    ]


def test_arxiv_entries_links_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed link fields
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_links == [
        ArxivMetadataLink("http://dx.doi.org/10.1140/epjc/s2003-01326-x", "text/html"),
        ArxivMetadataLink("http://arxiv.org/abs/hep-ex/0307015v1", "text/html"),
        ArxivMetadataLink("http://arxiv.org/pdf/hep-ex/0307015v1", "application/pdf"),
    ]
