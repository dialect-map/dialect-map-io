# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class BaseRemoteInput(metaclass=ABCMeta):
    """ Interface for the data input classes """

    @abstractmethod
    def request_paper(self, paper_id: str) -> dict:
        """
        Requests information about a certain Paper
        :param paper_id: paper ID
        :return: paper information
        """

        raise NotImplementedError()
