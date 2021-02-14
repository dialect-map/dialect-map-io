# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from typing import List


class BaseMetricsEngine(metaclass=ABCMeta):
    """ Interface for the NLP metrics computation """

    @abstractmethod
    def compute_abs_freq(self, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the absolute frequency (raw count of number of occurence) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'frequency': int }
        """
        pass

    @abstractmethod
    def compute_rel_freq(self, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the relative frequency (raw count / document length) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'frequency': float }
        """
        pass
