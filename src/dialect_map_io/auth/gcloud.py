# -*- coding: utf-8 -*-

from google.auth.credentials import Credentials as BaseCredentials
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2.service_account import IDTokenCredentials

from .base import BaseAuthenticator


class GCPAuthenticator(BaseAuthenticator):
    """Class defining GCP authentication basic methods"""

    def __init__(self, credentials: BaseCredentials):
        """
        Initiates the class with a provided Credentials object
        :param credentials: the provided Credentials object
        """

        self._credentials = credentials

    @property
    def credentials(self) -> BaseCredentials:
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

        return self._credentials.expired

    def refresh_token(self) -> str:
        """
        Refreshes and returns a new authorized token
        :return: new valid token
        """

        self._credentials.refresh(Request())
        return self._credentials.token


class DefaultAuthenticator(GCPAuthenticator):
    """Class implementing the default Service Account authentication with GCP"""

    def __init__(self, key_path: str):
        """
        Initiates a Credentials object using a Service Account key
        :param key_path: path to the Service Account key
        """

        super().__init__(
            Credentials.from_service_account_file(
                filename=key_path,
            )
        )


class OpenIDAuthenticator(GCPAuthenticator):
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

        super().__init__(
            IDTokenCredentials.from_service_account_file(
                filename=key_path,
                target_audience=target_url,
            )
        )
