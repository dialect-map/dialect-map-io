# -*- coding: utf-8 -*-
"""
This module will contain classes that generate NLP metrics (abs freq, rel freq, ...)
"""
from typing import List
from nlp.base import BaseMetricsEngine
import codecs
import string
from fuzzywuzzy import fuzz


class FuzzyMetricsEngine(BaseMetricsEngine):
    """Computing term frequency using fuzzy matching that allows for slight variations such as hyphen vs space,
    capital vs lower case, etc...
    """

    def __init__(self):
        # the text of the document is passed on instead of initialized as attribute
        # this facilitates interfacing with the map-reduce style pipeline for large number of documents
        pass

    @classmethod
    def compute_abs_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the absolute term frequency (raw count of number of occurrence) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': int }
        """
        text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
        tokens = cls.preprocess(text)  # tokenize

        return [{'jargon': " ".join(cls.preprocess(jargon)),
                 'tf': cls.phrase_count(cls.preprocess(jargon), tokens)}
                for jargon in terms]

    @classmethod
    def compute_bool_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        check if each jargon term is in the document
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': int }
        """
        text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
        tokens = cls.preprocess(text)  # tokenize

        return [{'jargon': " ".join(cls.preprocess(jargon)),
                 'tf': int(cls.phrase_count(cls.preprocess(jargon), tokens) >= 1)}
                for jargon in terms]

    @classmethod
    def compute_rel_freq(cls, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the relative term frequency (raw count / document length) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'tf': float }
        """
        text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
        tokens = cls.preprocess(text)  # tokenize

        return [{'jargon': " ".join(cls.preprocess(jargon)),
                 'tf': cls.phrase_count(cls.preprocess(jargon), tokens) / len(tokens)}
                for jargon in terms]

    @staticmethod
    def preprocess(document: str) -> List[str]:
        """
        simple tokenization
        INPUT: a string
        OUTPUT: a list of token
            tokenize, lower case,
            remove punctuations: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', and new line character
        note:
            pure numerics are allowed, in case searching for 3D in "3 D"
            single characters, stopwords are allowed

        """
        result = []

        # replace punctuation with white space
        document = document.lower().replace("’", " ").replace("'", " ").replace("\n", " ").translate(
            str.maketrans(string.punctuation, " " * len(string.punctuation)))

        for token in document.split():
            result.append(token)

        return result

    @staticmethod
    def phrase_count(phrase: List[str], tokens: List[str], similarity: int = 85) -> int:
        """count the number of occurrence of phrases a tokenized document
        both phrase and tokens must be list of str and have been cleaned by preprocess
        similarity: min levenshtein similarity ratio to accept a match
        https://medium.com/@shivendra15/nlp-approximate-phrase-matching-5a7f79bef9b8
         """

        count = 0
        len_phrase = len(phrase)

        for i in range(len(tokens) - len_phrase + 1):
            ngram = ""
            j = 0
            for j in range(i, i + len_phrase):
                ngram = ngram + " " + tokens[j]
            ngram = ngram.strip()
            if not ngram == "":
                if fuzz.ratio(ngram, " ".join(phrase)) > similarity:
                    # print([ngram, phrase, i, j, fuzz.ratio(ngram, " ".join(phrase)) ])
                    count = count + 1
        return count
