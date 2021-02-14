# -*- coding: utf-8 -*-
"""
This module will contain classes that generate NLP metrics (abs freq, rel freq, ...)
"""
from typing import List
from nlp.base import BaseMetricsEngine
import codecs
import string
from fuzzywuzzy import fuzz


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


def phrase_count(phrase: List[str], tokens: List[str], similarity: int = 85) -> int:
    """count the number of occurrence of phrases a tokenized document
    both phrase and tokens must be list of str and have been cleaned by preprocess
    similarity: min levenshtein similarity ratio to accept a match
    https://medium.com/@shivendra15/nlp-approximate-phrase-matching-5a7f79bef9b8
     """

    count = 0
    len_phrase = len(phrase)

    for i in range(len(tokens)-len_phrase+1):
        ngram = ""
        j = 0
        for j in range(i, i+len_phrase):
            ngram = ngram+" "+tokens[j]
        ngram = ngram.strip()
        if not ngram == "":
            if fuzz.ratio(ngram, " ".join(phrase)) > similarity:
                #print([ngram, phrase, i, j, fuzz.ratio(ngram, " ".join(phrase)) ])
                count = count + 1
    return count


class FuzzyMetricsEngine(BaseMetricsEngine):

    def __init__(self):
        pass

    def compute_abs_freq(self, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the absolute frequency (raw count of number of occurence) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'frequency': int }
        """
        text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
        tokens = preprocess(text)  # tokenize

        return [{'jargon': " ".join(preprocess(jargon)),
                 'tf_raw': phrase_count(preprocess(jargon), tokens)}
                for jargon in terms]

    def compute_rel_freq(self, terms: List[str], text: str) -> List[dict]:
        """
        Calculates the relative frequency (raw count / document length) of the given term
        :param terms: list of jargon term to compute the frequency about
        :param text: text of the document
        :return: a list of dictionary , each corresponds to a jargon { 'jargon': str, 'frequency': float }
        """
        text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
        tokens = preprocess(text)  # tokenize

        return [{'jargon': " ".join(preprocess(jargon)),
                 'tf_norm': phrase_count(preprocess(jargon), tokens) / len(tokens)}
                for jargon in terms]
