# -*- coding: utf-8 -*-

from datetime import datetime
from google.oauth2.service_account import IDTokenCredentials
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials

from .base import BaseAuthenticator


class OpenIDAuthenticator(BaseAuthenticator):
    """
    Class implementing the OpenID Connect authentication protocol with GCP
    Protocol reference: https://openid.net/connect/
    GCP documentation: https://google-auth.readthedocs.io/en/latest/index.html
    """

    def __init__(self, key_path: str, target_url: str):
        """
        Initiates a IDTokenCredentials object using a Service Account key
        :param key_path: path to the Service Account key
        :param target_url: URL authenticating against
        """

        self._credentials = IDTokenCredentials.from_service_account_file(
            filename=key_path,
            target_audience=target_url,
        )

    @property
    def credentials(self) -> Credentials:
        """
        Credentials holding entity
        :return: Google Cloud credentials object
        """

        return self._credentials

    def check_expired(self) -> bool:
        """
        Checks if the current credentials have expired
        :return: whether the credentials have expired
        """

        expiry_date = self._credentials.expiry
        current_date = datetime.now()

        return expiry_date < current_date

    def refresh_token(self) -> str:
        """
        Refreshes and returns a new authorized token
        :return: new valid token
        """

        self._credentials.refresh(Request())
        return self._credentials.token
