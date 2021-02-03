# -*- coding: utf-8 -*-

from .base import BaseAuthenticator


class DummyAuthenticator(BaseAuthenticator):
    """ Class defining a dummy authentication (useful when the API is public) """

    def check_expiration(self) -> bool:
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
