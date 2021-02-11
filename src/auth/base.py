# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class BaseAuthenticator(metaclass=ABCMeta):
    """ Interface for the API authenticator classes """

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
