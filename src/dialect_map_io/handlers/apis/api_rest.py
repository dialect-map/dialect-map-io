# -*- coding: utf-8 -*-

import logging

from typing import Callable

from requests import get as http_get
from requests import patch as http_patch
from requests import post as http_post
from requests import HTTPError
from requests import Response

from .base import BaseAPIHandler
from ...encoding import BaseDecoder
from ...encoding import BaseEncoder


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
