# -*- coding: utf-8 -*-

import logging
import time

from datetime import datetime
from typing import Callable

from requests import get as http_get
from requests import patch as http_patch
from requests import post as http_post
from requests import HTTPError
from requests import Response

from .base import BaseAPIHandler
from ...auth import BaseAuthenticator
from ...auth import DummyAuthenticator
from ...encoding import BaseDecoder
from ...encoding import BaseEncoder
from ...encoding import JSONPlainDecoder
from ...encoding import JSONPlainEncoder
from ...encoding import TXTPlainDecoder
from ...encoding import TXTPlainEncoder


logger = logging.getLogger()


class RestAPIHandler(BaseAPIHandler):
    """Class for dealing with REST APIs"""

    def __init__(self, base_url: str, decoder: BaseDecoder, encoder: BaseEncoder):
        """
        Initializes the API handler
        :param base_url: API complete URL
        :param decoder: API response decoder
        :param encoder: API request encoder
        """

        self._base_url = base_url.rstrip("/")
        self._decoder = decoder
        self._encoder = encoder

        self.headers = {}  # type: ignore

    @staticmethod
    def _check_response(response: Response) -> None:
        """
        Checks the status of the response for HTTP 4XX and 5XX codes
        :param response: raw API response
        """

        try:
            response.raise_for_status()
        except HTTPError:
            logger.error(f"The API response does not have a valid HTTP code")
            logger.error(f"Error: {response.text}")
            raise ConnectionError(response.text)

    def _perform_request(
        self,
        func: Callable,
        api_path: str,
        api_args: dict = None,
        api_data: dict = None,
    ) -> Response:
        """
        Performs an HTTP request to the given API path
        :param func: function to perform the HTTP request
        :param api_path: API path to send the request to
        :param api_args: API args to tune the request with
        :param api_data: API data to fill the request with
        :return: API response
        """

        api_path = api_path.strip("/")

        response = func(
            url=f"{self._base_url}/{api_path}",
            headers=self.headers,
            params=api_args,
            data=api_data,
        )

        self._check_response(response)
        return response

    def get_data(self, api_path: str, api_args: dict) -> object:
        """
        Requests data from a public API
        :param api_path: API path to send the request to
        :param api_args: API args to tune the request with
        :return: API response
        """

        resp = self._perform_request(http_get, api_path, api_args=api_args)
        resp = self._decoder.decode(resp.content)

        return resp

    def post_data(self, api_path: str, api_data: dict) -> object:
        """
        Posts data to a public API
        :param api_path: API path to send the request to
        :param api_data: API data to fill the request with
        :return: API response
        """

        data = self._encoder.encode(api_data)
        resp = self._perform_request(http_post, api_path, api_data=data)
        resp = self._decoder.decode(resp.content)

        return resp

    def patch_data(self, api_path: str) -> object:
        """
        Patches data from a public API
        :param api_path: API path to send the request to
        :return: API response
        """

        resp = self._perform_request(http_patch, api_path)
        resp = self._decoder.decode(resp.content)

        return resp


class ArxivAPIHandler(RestAPIHandler):
    """Class for dealing with the ArXiv API"""

    def __init__(self, wait_secs: int = 3, **kwargs):
        """
        Initializes the ArXiv API handler
        :param wait_secs: seconds to wait between API calls (optional)
        :kwargs: keyword arguments to pass to the parent class
        """

        super().__init__(
            decoder=TXTPlainDecoder(),
            encoder=TXTPlainEncoder(),
            **kwargs,
        )

        if not 0 <= wait_secs <= 60:
            raise ValueError("The waiting time must be between 0 and 60 seconds")

        self.wait_secs = wait_secs
        self.last_call = datetime.now()

    def _sleep_between_calls(self) -> None:
        """
        Wait time before the potentially next API call
        Ref: https://arxiv.org/help/api/user-manual
        """

        last_call_time = datetime.now()
        last_call_delta = last_call_time - self.last_call
        waiting_seconds = self.wait_secs - last_call_delta.total_seconds()

        if waiting_seconds > 0:
            time.sleep(waiting_seconds)

        self.last_call = last_call_time

    def _perform_request(self, *args, **kwargs) -> Response:
        """
        Performs an HTTP request to the given API path
        :param args: positional arguments to pass to the parent method
        :param kwargs: keyword arguments to pass to the parent method
        :return: API response
        """

        self._sleep_between_calls()

        return super()._perform_request(*args, **kwargs)

    def request_metadata(self, paper_id: str) -> str:
        """
        Requests metadata about a certain Paper
        :param paper_id: paper ID
        :return: paper metadata
        """

        resp = self.get_data("query", {"id_list": paper_id})

        assert isinstance(resp, str)
        return resp


class DialectMapAPIHandler(RestAPIHandler):
    """Class for dealing with the Dialect map APIs"""

    def __init__(self, auth_ctl: BaseAuthenticator = None, **kwargs):
        """
        Initializes the Dialect map API handler
        :param auth_ctl: authenticator controller (optional)
        :kwargs: keyword arguments to pass to the parent class
        """

        super().__init__(
            decoder=JSONPlainDecoder(),
            encoder=JSONPlainEncoder(),
            **kwargs,
        )

        if auth_ctl is None:
            auth_ctl = DummyAuthenticator()

        self.auth_ctl = auth_ctl
        self.auth_token = auth_ctl.refresh_token()

    def _update_auth_header(self) -> None:
        """
        Updates the headers with the API authentication token
        Ref: https://datatracker.ietf.org/doc/html/rfc6750
        """

        if not self.auth_ctl.check_expired():
            return

        self.auth_token = self.auth_ctl.refresh_token()
        self.headers["Authorization"] = f"Bearer {self.auth_token}"

    def _perform_request(self, *args, **kwargs) -> Response:
        """
        Performs an HTTP request to the given API path
        :param args: positional arguments to pass to the parent method
        :param kwargs: keyword arguments to pass to the parent method
        :return: API response
        """

        self._update_auth_header()

        return super()._perform_request(*args, **kwargs)

    def create_record(self, api_path: str, record: dict) -> dict:
        """
        Creates a record via POST request to the specified API path
        :param api_path: API path to send the request
        :param record: the record itself
        :return: JSON-decoded response
        """

        resp = self.post_data(api_path, record)

        assert isinstance(resp, dict)
        return resp

    def archive_record(self, api_path: str) -> dict:
        """
        Archives a record via PATCH request to the specified API path
        :param api_path: API path to send the request
        :return: JSON-decoded response
        """

        resp = self.patch_data(api_path)

        assert isinstance(resp, dict)
        return resp
