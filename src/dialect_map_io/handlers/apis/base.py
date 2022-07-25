# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod


class BaseAPIHandler(ABC):
    """Interface for the API handler classes"""

    @abstractmethod
    def get_data(self, api_path: str, api_args: dict) -> object:
        """
        Requests data from a public API
        :param api_path: API path to send the request
        :param api_args: API args to tune the request
        :return: API response
        """

        raise NotImplementedError()

    @abstractmethod
    def post_data(self, api_path: str, record: dict) -> object:
        """
        Posts data to a public API
        :param api_path: API path to send the request
        :param record: data to be posted
        :return: API response
        """

        raise NotImplementedError()

    @abstractmethod
    def patch_data(self, api_path: str) -> object:
        """
        Patches data from a public API
        :param api_path: API path to send the request
        :return: API response
        """

        raise NotImplementedError()
