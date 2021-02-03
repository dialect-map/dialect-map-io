# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class BaseDataOutput(metaclass=ABCMeta):
    """ Interface for the data output classes """

    @abstractmethod
    def send_category(self, category_data: dict) -> str:
        """
        Sends information about a certain Category to a data persistent layer
        :param category_data: specific Category fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_jargon(self, jargon_data: dict) -> str:
        """
        Sends information about a certain Jargon to a data persistent layer
        :param jargon_data: specific Jargon fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_jargon_group(self, group_data: dict) -> str:
        """
        Sends information about a certain Jargon group to a data persistent layer
        :param group_data: specific Jargon group fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_paper(self, paper_data: dict) -> str:
        """
        Sends information about a certain Paper to a data persistent layer
        :param paper_data: specific Paper fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_paper_author(self, author_data: dict) -> str:
        """
        Sends information about a certain Author to a data persistent layer
        :param author_data: specific Author fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_paper_counters(self, counters_data: dict) -> str:
        """
        Sends information about certain Paper ref. counters to a data persistent layer
        :param counters_data: specific Paper ref. counters fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_paper_membership(self, membership_data: dict) -> str:
        """
        Sends information about certain Paper membership to a data persistent layer
        :param membership_data: specific Paper membership fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_metrics_category(self, metrics_data: dict) -> str:
        """
        Sends information about certain Category metrics to a data persistent layer
        :param metrics_data: specific Category metrics fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_metrics_paper(self, metrics_data: dict) -> str:
        """
        Sends information about certain Paper metrics to a data persistent layer
        :param metrics_data: specific Paper metrics fields
        :return: ID of the saved record
        """

        raise NotImplementedError()

    @abstractmethod
    def send_reference(self, reference_data: dict) -> str:
        """
        Sends information about certain Paper reference to a data persistent layer
        :param reference_data: specific Paper reference fields
        :return: ID of the saved record
        """

        raise NotImplementedError()
