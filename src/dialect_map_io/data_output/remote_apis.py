# -*- coding: utf-8 -*-

import logging
import requests

from abc import ABC
from abc import abstractmethod
from requests import Response
from typing import Callable

from ..auth import BaseAuthenticator
from ..auth import DummyAuthenticator

logger = logging.getLogger()


class BaseOutputAPI(ABC):
    """Interface for the API data output classes"""

    @abstractmethod
    def create_record(self, api_path: str, record: dict) -> dict:
        """
        Sends a record information to a data persistent layer URL
        :param api_path: remote host API endpoint
        :param record: the record itself
        :return: JSON-encoded response
        """

        raise NotImplementedError()

    @abstractmethod
    def archive_record(self, api_path: str) -> dict:
        """
        Sends a record archive order through a data persistence layer URL
        :param api_path: remote host API endpoint
        :return: JSON-encoded response
        """

        raise NotImplementedError()


class RestOutputAPI(BaseOutputAPI):
    """Class for sending data to REST APIs"""

    def __init__(self, base_url: str, auth_ctl: BaseAuthenticator = None):
        """
        Initializes the remote API output reference
        :param base_url: remote API complete URL
        :param auth_ctl: authenticator controller (optional)
        """

        if auth_ctl is None:
            auth_ctl = DummyAuthenticator()

        self.auth_ctl = auth_ctl
        self.base_url = base_url.rstrip("/")
        self.api_token = auth_ctl.refresh_token()

    @staticmethod
    def _check_response(response: Response) -> None:
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

    def _perform_request(self, func: Callable, api_path: str, api_data: dict) -> Response:
        """
        Performs a HTTP request to the given API path
        :param func: function to perform the HTTP request
        :param api_path: API path to send the request
        :param api_data: JSON data to send in the request
        :return: API response
        """

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": f"application/json; charset=utf-8",
        }

        response = func(
            url=f"{self.base_url}{api_path}",
            headers=headers,
            json=api_data,
        )

        self._check_response(response)
        return response

    def _refresh_token(self) -> None:
        """
        Updates the API token and request headers
        :return: None
        """

        if self.auth_ctl.check_expired():
            self.api_token = self.auth_ctl.refresh_token()

    def create_record(self, api_path: str, record: dict) -> dict:
        """
        Sends a record information to a data persistent layer URL
        :param api_path: remote host API endpoint
        :param record: the record itself
        :return: JSON-encoded response
        """

        self._refresh_token()

        resp = self._perform_request(requests.post, api_path, record)
        resp = self._decode_response(resp)
        return resp

    def archive_record(self, api_path: str) -> dict:
        """
        Sends a record archive order through a data persistence layer URL
        :param api_path: remote host API endpoint
        :return: JSON-encoded response
        """

        self._refresh_token()

        resp = self._perform_request(requests.patch, api_path, {})
        resp = self._decode_response(resp)
        return resp
