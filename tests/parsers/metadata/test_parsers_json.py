# -*- coding: utf-8 -*-

import json
import pytest
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timezone

from src.dialect_map_io.models import ArxivMetadata
from src.dialect_map_io.models import ArxivMetadataAuthor
from src.dialect_map_io.parsers import JSONMetadataParser

from ...__paths import META_JSON_FOLDER


def load_metadata_json(file_name: str) -> ArxivMetadata:
    """
    Loads a metadata JSON sample given its file name
    :param file_name: name of the sample file
    :return: metadata object
    """

    json_parser = JSONMetadataParser()

    json_file = META_JSON_FOLDER.joinpath(file_name)
    json_text = open(json_file, "r").read()
    json_dict = json.loads(json_text)
    json_objs = json_parser.parse_body(json_dict)

    return json_objs[0]


@pytest.fixture(scope="module")
def json_entry_1() -> ArxivMetadata:
    """
    JSON metadata object parsed from a sample JSON
    :return: metadata object
    """

    return load_metadata_json("entry_1.json")


@pytest.fixture(scope="module")
def json_entry_2() -> ArxivMetadata:
    """
    JSON metadata object parsed from a sample JSON
    :return: metadata object
    """

    return load_metadata_json("entry_2.json")


@pytest.fixture(scope="module")
def json_entry_3() -> ArxivMetadata:
    """
    JSON metadata object parsed from a sample JSON
    :return: metadata object
    """

    return load_metadata_json("entry_3.json")


def test_json_entries_parse(
    json_entry_1: ArxivMetadata,
    json_entry_2: ArxivMetadata,
    json_entry_3: ArxivMetadata,
):
    """
    Tests the correct parsing of the Arxiv json entries fields
    :param json_entry_1: metadata object
    :param json_entry_2: metadata object
    :param json_entry_3: metadata object
    """

    assert json_entry_1.paper_id == "0704.0001"
    assert json_entry_1.paper_rev == "v1"
    assert json_entry_1.paper_doi == "10.1103/PhysRevD.76.013009"
    assert json_entry_1.paper_category == "hep-ph"

    assert json_entry_2.paper_id == "0704.0002"
    assert json_entry_2.paper_rev == "v1"
    assert json_entry_2.paper_doi == ""
    assert json_entry_2.paper_category == "math.CO"

    assert json_entry_3.paper_id == "supr-con/9609003"
    assert json_entry_3.paper_rev == "v1"
    assert json_entry_3.paper_doi == "10.1143/JPSJ.65.3131"
    assert json_entry_3.paper_category == "supr-con"


def test_json_created_date_parse(
    json_entry_1: ArxivMetadata,
    json_entry_2: ArxivMetadata,
    json_entry_3: ArxivMetadata,
):
    """
    Tests the correct parsing of the Arxiv json created_at field
    :param json_entry_1: metadata object
    :param json_entry_2: metadata object
    :param json_entry_3: metadata object
    """

    # Created: "Mon, 2 Apr 2007 19:18:42 GMT"
    assert json_entry_1.paper_created_at == datetime.combine(
        date=date(2007, 4, 2),
        time=time(19, 18, 42),
        tzinfo=timezone.utc,
    )

    # Created: "Sat, 31 Mar 2007 02:26:18 GMT"
    assert json_entry_2.paper_created_at == datetime.combine(
        date=date(2007, 3, 31),
        time=time(2, 26, 18),
        tzinfo=timezone.utc,
    )

    # Created: "Wed, 18 Sep 1996 07:57:29 GMT"
    assert json_entry_3.paper_created_at == datetime.combine(
        date=date(1996, 9, 18),
        time=time(7, 57, 30),
        tzinfo=timezone.utc,
    )


def test_json_updated_date_parse(
    json_entry_1: ArxivMetadata,
    json_entry_2: ArxivMetadata,
    json_entry_3: ArxivMetadata,
):
    """
    Tests the correct parsing of the Arxiv json updated_at field
    :param json_entry_1: metadata object
    :param json_entry_2: metadata object
    :param json_entry_3: metadata object
    """

    # Updated: "Mon, 2 Apr 2007 19:18:42 GMT"
    assert json_entry_1.paper_updated_at == datetime.combine(
        date=date(2007, 4, 2),
        time=time(19, 18, 42),
        tzinfo=timezone.utc,
    )

    # Updated: "Sat, 31 Mar 2007 02:26:18 GMT"
    assert json_entry_2.paper_updated_at == datetime.combine(
        date=date(2007, 3, 31),
        time=time(2, 26, 18),
        tzinfo=timezone.utc,
    )

    # Updated: "Wed, 18 Sep 1996 07:57:29 GMT"
    assert json_entry_3.paper_updated_at == datetime.combine(
        date=date(1996, 9, 18),
        time=time(7, 57, 30),
        tzinfo=timezone.utc,
    )


def test_json_authors_parse(
    json_entry_1: ArxivMetadata,
    json_entry_2: ArxivMetadata,
    json_entry_3: ArxivMetadata,
):
    """
    Tests the correct parsing of the Arxiv json authors field
    :param json_entry_1: metadata object
    :param json_entry_2: metadata object
    :param json_entry_3: metadata object
    """

    assert json_entry_1.paper_authors == [
        ArxivMetadataAuthor("Bal\u00e1zs C."),
        ArxivMetadataAuthor("Berger E. L."),
        ArxivMetadataAuthor("Nadolsky P. M."),
        ArxivMetadataAuthor("Yuan C. -P."),
    ]

    assert json_entry_2.paper_authors == [
        ArxivMetadataAuthor("Streinu Ileana"),
        ArxivMetadataAuthor("Theran Louis"),
    ]

    assert json_entry_3.paper_authors == [
        ArxivMetadataAuthor("Hasegawa Yasumasa Himeji Institute of Technology"),
    ]
