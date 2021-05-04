# -*- coding: utf-8 -*-

import logging
import requests
import time

from abc import ABC
from abc import abstractmethod
from requests import Response

logger = logging.getLogger()


class BaseInputAPI(ABC):
    """Interface for the API data input classes"""

    @abstractmethod
    def request_data(self, api_path: str, api_args: dict):
        """
        Requests data from a public API
        :param api_path: API path to send the request
        :param api_args: API args to tune the request
        :return: data
        """

        raise NotImplementedError()


class ArxivInputAPI(BaseInputAPI):
    """Class for the ArXiv API data retrieval"""

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
    def _check_response(response: Response):
        """
        Checks the status of the response for HTTP 4XX and 5XX codes
        :param response: raw API response
        """

        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.error(f"The API response does not have a valid HTTP code")
            logger.error(f"Error: {response.text}")
            raise ConnectionError(response.text)

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

        self._check_response(response)
        return response

    def request_data(self, api_path: str, api_args: dict) -> str:
        """
        Requests feed data from the ArXiv public API
        :param api_path: API path to send the request
        :param api_args: API args to tune the request
        :return: raw feed data
        """

        resp = self._perform_request(api_path, api_args)
        resp = self._decode_response(resp)
        return resp

    def request_paper(self, paper_id: str) -> str:
        """
        Requests information about a certain Paper
        :param paper_id: paper ID
        :return: paper information
        """

        return self.request_data("/query", {"id_list": paper_id})


class RestInputAPI(BaseInputAPI):
    """Class for requesting data from REST APIs"""

    def __init__(self, base_url: str):
        """
        Initializes the remote API input reference
        :param base_url: remote API complete URL
        """

        self.base_url = base_url.rstrip("/")

    @staticmethod
    def _check_response(response: Response):
        """
        Checks the status of the response for HTTP 4XX and 5XX codes
        :param response: raw API response
        """

        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.error(f"The API response does not have a valid HTTP code")
            logger.error(f"Error: {response.text}")
            raise ConnectionError(response.text)

    @staticmethod
    def _decode_response(response: Response) -> dict:
        """
        Decodes the response assuming a serialized JSON
        :param response: raw API response
        :return: dictionary API response
        """

        try:
            json = response.json()
        except ValueError:
            logger.error(f"The API response does not contains a valid JSON")
            logger.error(f"Response: {response.text}")
            raise
        else:
            return json

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

        self._check_response(response)
        return response

    def request_data(self, api_path: str, api_args: dict) -> dict:
        """
        Requests JSON data from a public API
        :param api_path: API path to send the request
        :param api_args: API args to tune the request
        :return: JSON-encoded response
        """

        resp = self._perform_request(api_path, api_args)
        resp = self._decode_response(resp)
        return resp
