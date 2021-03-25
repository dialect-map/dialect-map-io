# -*- coding: utf-8 -*-

import logging
import re

from abc import ABC
from abc import abstractmethod
import dateutil.parser
from datetime import datetime
from datetime import timezone
from feedparser import FeedParserDict
from feedparser import parse as feed_parse
from typing import List

from ..models import ArxivFeedHeader
from ..models import ArxivFeedEntry
from ..models import ArxivFeedEntryAuthor
from ..models import ArxivFeedEntryLink

logger = logging.getLogger()


class BaseFeedParser(ABC):
    """ Interface for the feed string parser classes """

    @abstractmethod
    def parse_header(self, feed: str) -> ArxivFeedHeader:
        """
        Parses the header fields of a given feed result
        :param feed: string with the feed result
        :return: top-level fields data object
        """

        raise NotImplementedError()

    @abstractmethod
    def parse_entries(self, feed: str) -> List[ArxivFeedEntry]:
        """
        Parses the entry sections of a given feed result
        :param feed: string with the feed result
        :return: parsed entries data objects
        """

        raise NotImplementedError()


class ArxivFeedParser(BaseFeedParser):
    """
    Class implementing the Atom 1.0 parsing functionality for the ArXiv feed
    Atom reference: https://www.ietf.org/rfc/rfc4287.txt
    ArXiv feed: https://arxiv.org/help/api/user-manual#52-details-of-atom-results-returned
    """

    def __init__(self):
        """ Initializes the Arxiv feed parser object """

        self.entry_id_prefix = re.compile(r"http://arxiv.org/abs/")
        self.entry_id_suffix = re.compile(r"v\d+")

    @staticmethod
    def _parse_date(date_string: str) -> datetime:
        """
        Parses a date string to a UTC datetime object
        :param date_string: ArXiv date in string format
        :return: UTC datetime object
        """

        try:
            utc_date = dateutil.parser.isoparse(date_string)
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

        return re.sub(r"\s\s+", " ", long_string)

    @staticmethod
    def _parse_links(link_entries: list) -> List[str]:
        """
        Parses and extracts a link href attributes from the feed
        :param link_entries: list encapsulating current level links
        :return: link URLs
        """

        return [link.href for link in link_entries]

    def _extract_id(self, entry_id: str) -> str:
        """
        Extract the paper ID from the value found on the <entry>.<id> field
        :param entry_id: value found on <entry>.<id>
        :return: paper ID
        """

        id = entry_id
        id = re.sub(self.entry_id_prefix, "", id, count=1)
        id = re.sub(self.entry_id_suffix, "", id, count=1)
        return id

    def _extract_rev(self, entry_id: str) -> str:
        """
        Extract the paper revision from the value found on the <entry>.<id> field
        :param entry_id: value found on <entry>.<id>
        :return: paper revision
        """

        rev = re.search(self.entry_id_suffix, entry_id)
        rev = rev[0] if rev is not None else "1"
        return rev

    def _extract_doi(self, entry: FeedParserDict) -> str:
        """
        Extract the paper DOI from the value found on the <entry> structure
        :param entry: feed <entry> structure
        :return: paper DOI
        """

        try:
            paper_doi = entry.arxiv_doi
        except AttributeError:
            paper_doi = ""
            paper_id = self._extract_id(entry.id)
            logger.info(f"Paper {paper_id} does not specify a DOI")

        return paper_doi

    def parse_header(self, feed: str) -> ArxivFeedHeader:
        """
        Parses the header fields of a given feed result
        :param feed: string with the feed result
        :return: top-level fields data object
        """

        parsed = feed_parse(feed)

        return ArxivFeedHeader(
            query_id=parsed.feed.id,
            query_url=self._parse_links(parsed.feed.links)[0],
            results_ts=self._parse_date(parsed.feed.updated),
        )

    def parse_entries(self, feed: str) -> List[ArxivFeedEntry]:
        """
        Parses the entry sections of a given feed result
        :param feed: string with the feed result
        :return: parsed entries data objects
        """

        papers = []
        parsed = feed_parse(feed)

        for entry in parsed.entries:
            category = entry.arxiv_primary_category["term"]
            authors = [ArxivFeedEntryAuthor(author.name) for author in entry.authors]
            links = [ArxivFeedEntryLink(l["href"], l["type"]) for l in entry.links]

            paper = ArxivFeedEntry(
                paper_id=self._extract_id(entry.id),
                paper_rev=self._extract_rev(entry.id),
                paper_title=self._parse_string(entry.title),
                paper_description=self._parse_string(entry.summary),
                paper_doi=self._extract_doi(entry),
                paper_category=category,
                paper_authors=authors,
                paper_links=links,
                paper_created_at=self._parse_date(entry.published),
                paper_updated_at=self._parse_date(entry.updated),
            )

            papers.append(paper)

        return papers
