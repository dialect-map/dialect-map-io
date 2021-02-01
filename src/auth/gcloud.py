# -*- coding: utf-8 -*-

from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

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

        self.credentials = service_account.IDTokenCredentials.from_service_account_file(
            filename=key_path,
            target_audience=target_url,
        )

    def check_expiration(self) -> bool:
        """
        Checks if the current credentials have expired
        :return: whether the credentials have expired
        """

        expiry_date = self.credentials.expiry
        current_date = datetime.now()

        return expiry_date < current_date

    def refresh_token(self) -> str:
        """
        Refreshes and returns a new authorized token
        :return: new valid token
        """

        self.credentials.refresh(Request())
        return self.credentials.token
