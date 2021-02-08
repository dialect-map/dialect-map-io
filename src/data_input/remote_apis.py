# -*- coding: utf-8 -*-

import requests
import time
import urllib.parse as urlparse

from .base import BaseRemoteInput


class ArxivAPI(BaseRemoteInput):
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

    def _perform_request(self, api_path: str, api_args: dict) -> str:
        """
        Performs a HTTP GET request to the given API path
        :param api_path: API endpoint to send the request
        :param api_args: API arguments to tune the request
        :return: response
        """

        args = urlparse.urlencode(api_args)
        resp = requests.get(f"{self.base_url}/{api_path}?{args}")
        resp.raise_for_status()

        # Wait time before the potentially next API call
        # Ref: https://arxiv.org/help/api/user-manual
        time.sleep(self.wait_secs)

        return resp.text

    def request_paper(self, paper_id: str) -> str:
        """
        Requests information about a certain Paper
        :param paper_id: paper ID
        :return: paper information
        """

        return self._perform_request(
            api_path="query",
            api_args={"id_list": paper_id},
        )
