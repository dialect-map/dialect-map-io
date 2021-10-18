# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ArxivMetadataAuthor:
    """
    Object containing the author field of an Arxiv metadata entry

    :attr name: name of the author
    """

    name: str


@dataclass
class ArxivMetadataLink:
    """
    Object containing the link fields of an Arxiv metadata entry

    :attr resource_url: resource URL assigned to the provided link
    :attr resource_type: resource type assigned to the provided link
    """

    resource_url: str
    resource_type: str


@dataclass
class ArxivMetadata:
    """
    Object containing the fields of an Arxiv metadata entry

    :attr paper_id: unique identifier
    :attr paper_rev: unique revision
    :attr paper_title: paper title
    :attr paper_summary: paper summary description
    :attr paper_category: paper main category
    :attr paper_doi: DOI identifier
    :attr paper_authors: authors list
    :attr paper_links: resources links list
    :attr paper_created_at: paper submission date
    :attr paper_updated_at: paper updated date (same as created in revision #1)
    """

    paper_id: str
    paper_rev: str
    paper_title: str
    paper_description: str
    paper_category: str
    paper_doi: str
    paper_authors: List[ArxivMetadataAuthor]
    paper_links: List[ArxivMetadataLink]
    paper_created_at: datetime
    paper_updated_at: datetime
