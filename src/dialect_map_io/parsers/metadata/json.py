# -*- coding: utf-8 -*-

import logging
import pytz
import re

from datetime import datetime
from datetime import timezone
from typing import List

from .base import BaseMetadataParser
from ...models import ArxivMetadata
from ...models import ArxivMetadataAuthor

logger = logging.getLogger()


class JSONMetadataParser(BaseMetadataParser):
    """
    Class implementing the JSON parsing functionality for the ArXiv JSON-based metadata
    Kaggle reference: https://www.kaggle.com/Cornell-University/arxiv
    """

    def __init__(self):
        """Initializes the Arxiv json metadata parser object"""

        self.dates_format = "%a, %d %b %Y %H:%M:%S %Z"
        self.version_regex = re.compile(r"v\d+")

    @staticmethod
    def _parse_date(date_string: str) -> datetime:
        """
        Parses a date string to a UTC datetime object
        :param date_string: ArXiv date in string format
        :return: UTC datetime object
        """

        try:
            off_date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            utc_date = datetime.fromtimestamp(off_date.timestamp(), timezone.utc)
        except Exception as err:
            logger.error(err)
            raise err

        return utc_date

    @staticmethod
    def _parse_string(long_string: str) -> str:
        """
        Parses and cleans a potentially multi-line string
        :param long_string: potentially multi-line string
        :return: trimmed string
        """

        return re.sub(r"\s\s+", " ", long_string).strip()

    def _extract_date(self, date: str) -> datetime:
        """
        Parses a date string to a UTC datetime object
        :param date: string date to parse
        :return: UTC datetime object
        """

        # Extracting the timezone out of the string
        dt = date[:-3].strip()
        tz = date[-3:].strip()

        # Pruning the timezone out of the format
        fmt = self.dates_format[:-3]

        off_date = datetime.strptime(dt, fmt)
        off_date = off_date.replace(tzinfo=pytz.timezone(tz))
        utc_date = self._parse_date(off_date.isoformat())

        return utc_date

    def _extract_rev(self, version: str) -> str:
        """
        Extract the paper revision from the value found on the versions field
        :param version: value found in the versions field
        :return: paper revision
        """

        rev = re.search(self.version_regex, version)
        rev = rev[0] if rev is not None else "1"
        return rev

    def _extract_doi(self, entry: dict) -> str:
        """
        Extract and logs the paper DOI from the value found on the JSON entry
        :param entry: value found in the JSON entry
        :return: paper DOI
        """

        paper_doi = entry["doi"]

        if paper_doi is None:
            paper_doi = ""
            paper_id = entry["id"]
            logger.info(f"Paper {paper_id} does not specify a DOI")

        return paper_doi

    def parse_header(self, entry: dict) -> None:
        """Metadata JSON has not header. Returns None"""

        return None

    def parse_body(self, entry: dict) -> List[ArxivMetadata]:
        """
        Parses the metadata fields of a given metadata JSON entry
        :param entry: metadata fields of a given paper
        :return: parsed metadata objects
        """

        papers = []
        created = None

        for version in entry["versions"]:
            categories = entry["categories"].split()
            created = self._extract_date(version["created"]) if created is None else created
            updated = self._extract_date(version["created"])
            authors = [self._parse_string(" ".join(author)) for author in entry["authors_parsed"]]
            authors = [ArxivMetadataAuthor(author) for author in authors]
            links = []  # type: ignore

            paper = ArxivMetadata(
                paper_id=entry["id"],
                paper_rev=self._extract_rev(version["version"]),
                paper_title=self._parse_string(entry["title"]),
                paper_description=self._parse_string(entry["abstract"]),
                paper_doi=self._extract_doi(entry),
                paper_category=categories[0],
                paper_authors=authors,
                paper_links=links,
                paper_created_at=created,
                paper_updated_at=updated,
            )

            papers.append(paper)

        return papers
