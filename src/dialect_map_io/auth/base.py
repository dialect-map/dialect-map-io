# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod


class BaseAuthenticator(ABC):
    """Interface for the API authenticator classes"""

    @property
    @abstractmethod
    def credentials(self):
        """Credentials holding entity"""

        raise NotImplementedError()

    @abstractmethod
    def check_expired(self) -> bool:
        """
        Checks if the current credentials have expired
        :return: whether the credentials have expired
        """

        raise NotImplementedError()

    @abstractmethod
    def refresh_token(self) -> str:
        """
        Refreshes and returns a new authorized token
        :return: new valid token
        """

        raise NotImplementedError()
