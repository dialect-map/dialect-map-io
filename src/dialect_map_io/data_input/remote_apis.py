# -*- coding: utf-8 -*-

import requests
import time

from abc import ABCMeta
from abc import abstractmethod
from requests import Response


class BaseAPIInput(metaclass=ABCMeta):
    """ Interface for the API data input classes """

    @abstractmethod
    def request_paper(self, paper_id: str) -> dict:
        """
        Requests information about a certain Paper
        :param paper_id: paper ID
        :return: paper information
        """

        raise NotImplementedError()


class ArxivAPI(BaseAPIInput):
    """ Class for the ArXiv API input data retrieval """

    def __init__(self, base_url: str, wait_secs: int = 3):
        """
        Initializes the ArXiv API input controller
        :param base_url: ArXiv API complete URL
        :param wait_secs: number of seconds to wait between API calls
        """

        if not 0 <= wait_secs <= 60:
            raise ValueError("The waiting time must be between 0 and 60 seconds")

        self.base_url = base_url.rstrip("/")
        self.wait_secs = wait_secs

    @staticmethod
    def _decode_response(response: Response) -> str:
        """
        Decodes the response assuming a non-JSON response
        :param response: raw API response
        :return: text API response
        """

        return response.text

    def _perform_request(self, api_path: str, api_args: dict) -> Response:
        """
        Performs a HTTP GET request to the given API path
        :param api_path: API path to send the request
        :param api_args: API args to tune the request
        :return: API response
        """

        response = requests.get(
            url=f"{self.base_url}{api_path}",
            params=api_args,
        )

        # Wait time before the potentially next API call
        # Ref: https://arxiv.org/help/api/user-manual
        time.sleep(self.wait_secs)

        response.raise_for_status()
        return response

    def request_paper(self, paper_id: str) -> str:
        """
        Requests information about a certain Paper
        :param paper_id: paper ID
        :return: paper information
        """

        resp = self._perform_request("/query", {"id_list": paper_id})
        resp = self._decode_response(resp)

        return resp
