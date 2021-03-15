# -*- coding: utf-8 -*-

from .base import BaseAuthenticator


class DummyAuthenticator(BaseAuthenticator):
    """ Class defining a dummy authentication (useful when the API is public) """

    @property
    def credentials(self) -> object:
        """
        Credentials holding entity
        :return: dummy object
        """

        return object()

    def check_expired(self) -> bool:
        """
        Checks if the current credentials have expired
        :return: False
        """

        return False

    def refresh_token(self) -> str:
        """
        Returns an empty token
        :return: empty string
        """

        return ""
