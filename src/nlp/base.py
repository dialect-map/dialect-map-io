# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class BaseMetricsEngine(metaclass=ABCMeta):
    """ Interface for the NLP metrics computation """

    @abstractmethod
    def compute_abs_freq(self, term: str) -> int:
        """
        Calculates the absolute frequency of the given term
        :param term: jargon term to compute the frequency about
        :return: number of occurrences
        """

        raise NotImplementedError()

    @abstractmethod
    def compute_rel_freq(self, term: str) -> float:
        """
        Calculates the relative frequency of the given term
        :param term: jargon term to compute the frequency about
        :return: relative frequency
        """

        raise NotImplementedError()
