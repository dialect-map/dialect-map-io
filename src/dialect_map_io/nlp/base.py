# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from typing import List


class BaseMetricsEngine(metaclass=ABCMeta):
    """ Interface for the NLP metrics computation """
    # these methods take in a list of jargon for each document
    # i.e. each document is open only once for all the listed jargon terms, to improve performance

    @classmethod
    @abstractmethod
    def compute_abs_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the absolute term frequency (raw count of number of occurence) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': int }
        """
        pass

    @classmethod
    @abstractmethod
    def compute_bool_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        check if each jargon term is in the document
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': int }
        """
        pass

    @classmethod
    @abstractmethod
    def compute_rel_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the relative term frequency (raw count / document length) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': float }
        """
        pass
