# -*- coding: utf-8 -*-

import logging
import requests

from abc import ABCMeta
from abc import abstractmethod
from requests import Response
from ..auth import BaseAuthenticator
from ..auth import DummyAuthenticator

logger = logging.getLogger()


class BaseAPIOutput(metaclass=ABCMeta):
    """ Interface for the API data output classes """

    @abstractmethod
    def send_record(self, api_path: str, record: dict) -> dict:
        """
        Sends a record information to a data persistent layer URL
        :param api_path: remote host API endpoint
        :param record: the record itself
        :return: JSON-encoded response
        """

        raise NotImplementedError()


class DialectMapAPI(BaseAPIOutput):
    """ Class for the data persistence Dialect Map API """

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
    def _decode_response(response: Response) -> dict:
        """
        Decodes the response assuming a serialized JSON
        :param response: raw API response
        :return: dictionary API response
        """

        try:
            json = response.json()
        except ValueError:
            logger.warning("The API did not respond with a valid JSON")
            json = {"response": response}

        return json

    def _perform_request(self, api_path: str, api_data: dict) -> Response:
        """
        Performs a HTTP POST request to the given API path
        :param api_path: API path to send the request
        :param api_data: JSON data to send in the request
        :return: API response
        """

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": f"application/json; charset=utf-8",
        }

        response = requests.post(
            url=f"{self.base_url}{api_path}",
            headers=headers,
            json=api_data,
        )

        response.raise_for_status()
        return response

    def _refresh_token(self) -> None:
        """
        Updates the API token and request headers
        :return: None
        """

        if self.auth_ctl.check_expired():
            self.api_token = self.auth_ctl.refresh_token()

    def send_record(self, api_path: str, record: dict) -> dict:
        """
        Sends a record information to a data persistent layer URL
        :param api_path: remote host API endpoint
        :param record: the record itself
        :return: JSON-encoded response
        """

        self._refresh_token()

        resp = self._perform_request(api_path, record)
        resp = self._decode_response(resp)
        return resp
