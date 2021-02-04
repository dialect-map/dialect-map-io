# -*- coding: utf-8 -*-

import requests

from .base import BaseDataOutput
from ..auth import BaseAuthenticator
from ..auth import DummyAuthenticator


class RemoteAPIOutput(BaseDataOutput):
    """ Class for the remote API data output persistence """

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
        self.api_headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": f"application/json; charset=utf-8",
        }

    def _refresh_token(self) -> None:
        """ Updates the API token and request headers """

        if self.auth_ctl.check_expiration() is False:
            return

        self.api_token = self.auth_ctl.refresh_token()
        self.api_headers["Authorization"] = f"Bearer {self.api_token}"

    def _perform_request(self, api_path: str, api_data: dict) -> str:
        """
        Performs a HTTP POST request to the given API path
        :param api_path: API endpoint to send the request
        :param api_data: JSON data to send in the request
        :return: record ID
        """

        self._refresh_token()

        resp = requests.post(
            url=f"{self.base_url}{api_path}",
            headers=self.api_headers,
            json=api_data,
        )

        resp.raise_for_status()
        json = resp.json()
        return json["id"]

    def send_category(self, category_data: dict) -> str:
        """
        Sends information about a certain Category to a data persistent layer
        :param category_data: specific Category fields
        :return: ID of the saved record
        """

        return self._perform_request(api_path="/category", api_data=category_data)

    def send_jargon(self, jargon_data: dict) -> str:
        """
        Sends information about a certain Jargon to a data persistent layer
        :param jargon_data: specific Jargon fields
        :return: ID of the saved record
        """

        return self._perform_request("/jargon", jargon_data)

    def send_jargon_group(self, group_data: dict) -> str:
        """
        Sends information about a certain Jargon group to a data persistent layer
        :param group_data: specific Jargon group fields
        :return: ID of the saved record
        """

        return self._perform_request("/jargon-group", group_data)

    def send_paper(self, paper_data: dict) -> str:
        """
        Sends information about a certain Paper to a data persistent layer
        :param paper_data: specific Paper fields
        :return: ID of the saved record
        """

        return self._perform_request("/paper", paper_data)

    def send_paper_author(self, author_data: dict) -> str:
        """
        Sends information about a certain Author to a data persistent layer
        :param author_data: specific Author fields
        :return: ID of the saved record
        """

        return self._perform_request("/paper/author", author_data)

    def send_paper_counters(self, counters_data: dict) -> str:
        """
        Sends information about certain Paper ref. counters to a data persistent layer
        :param counters_data: specific Paper ref. counters fields
        :return: ID of the saved record
        """

        return self._perform_request("/paper/reference/counters", counters_data)

    def send_paper_membership(self, membership_data: dict) -> str:
        """
        Sends information about certain Paper membership to a data persistent layer
        :param membership_data: specific Paper membership fields
        :return: ID of the saved record
        """

        return self._perform_request("/membership", membership_data)

    def send_metrics_category(self, metrics_data: dict) -> str:
        """
        Sends information about certain Category metrics to a data persistent layer
        :param metrics_data: specific Category metrics fields
        :return: ID of the saved record
        """

        return self._perform_request("/category/metrics", metrics_data)

    def send_metrics_paper(self, metrics_data: dict) -> str:
        """
        Sends information about certain Paper metrics to a data persistent layer
        :param metrics_data: specific Paper metrics fields
        :return: ID of the saved record
        """

        return self._perform_request("/paper/metrics", metrics_data)

    def send_reference(self, reference_data: dict) -> str:
        """
        Sends information about certain Paper reference to a data persistent layer
        :param reference_data: specific Paper reference fields
        :return: ID of the saved record
        """

        return self._perform_request("/reference", reference_data)
