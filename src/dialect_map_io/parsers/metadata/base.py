# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseMetadataParser(ABC):
    """Interface for the metadata parser classes"""

    @abstractmethod
    def parse_header(self, metadata: Any) -> object:
        """
        Parses the header fields of a metadata record
        :param metadata: external metadata record
        :return: top-level fields data object
        """

        raise NotImplementedError()

    @abstractmethod
    def parse_body(self, metadata: Any) -> object:
        """
        Parses the sections of a metadata record
        :param metadata: external metadata record
        :return: parsed metadata objects
        """

        raise NotImplementedError()
