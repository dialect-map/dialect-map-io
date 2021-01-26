import string
import codecs
import re
import json
from typing import List

from fuzzywuzzy import fuzz


# copy from https://github.com/quynhneo/detm-arxiv/blob/master/arxivtools/preprocessing.py
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
        str.maketrans(string.punctuation, " "*len(string.punctuation)))

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
                print([ngram, phrase, i, j, fuzz.ratio(ngram, " ".join(phrase)) ])
                count = count + 1
    return count


def terms_freq(jargons_list: List[str], text: str, similarity=85, method: str = 'norm') -> List[dict]:
    """ for each jargon in jargon lists, return a number of its occurrence in str content of text.
        both jargons and text are preprocess before counting
        similarity: min levenshtein similarity ratio to accept a match
        methods:
            raw: raw count
            bool: False for raw count = 0, True for count >= 1
            norm: raw count/ processed text length
    """

    text = codecs.decode(text, 'unicode_escape')  # convert \\n to \n in text so tokenizer knows to split
    tokens = preprocess(text)  # tokenize

    if method == 'raw':  # raw count
        return [{'jargon': " ".join(preprocess(jargon)),
                 'tf_raw': phrase_count(preprocess(jargon), tokens, similarity=similarity)}
                for jargon in jargons_list]

    if method == 'bool':
        return [{'jargon': " ".join(preprocess(jargon)),
                 'tf_bool': phrase_count(preprocess(jargon), tokens, similarity=similarity) >= 1}
                for jargon in jargons_list]

    if method == 'norm':
        return [{'jargon': " ".join(preprocess(jargon)),
                 'tf_norm': phrase_count(preprocess(jargon), tokens, similarity=similarity)/len(tokens)}
                for jargon in jargons_list]



def get_metadata(path_to_meta: str):
    with open(path_to_meta, 'r') as f:
        for line in f:
            yield line


def cat_look_up(id: str, path_to_meta: str):
    """(slow) look up category of paper id (no version included) from metadata"""
    metadata = get_metadata(path_to_meta)
    id = id.split('v')[0]  # remove version if included
    for paper in metadata:
        if json.loads(paper)['id'] == id:
            cat = json.loads(paper)['categories']
            return cat


def path2id(text: str) -> str:
    """ input: text string, containing the SPECIFIC str '(file:path, text)'
        output: id of the paper, None if f
    """
    # math file:path.txt, split by '/', get the last, remove extension
    match = re.search('file:.*?\.txt', text)  #.*? the shortest match
    if match:
        return match.group().split('/')[-1].strip('.txt')


def cat_parser(text: str) -> str:
    """ parse category from text
        input: text (str), containing SPECIFIC str '(file:path, text)'
        output: category (str) of the paper, None if the text doesn't contain category tag
    """
    # beginning of second part of tuple + something+ ID + something + [ category ]
    search_str = ',.*'+ path2id(text)+'.*?\[.*?\]'  # (.*?) the shortest match, any length, between []
    match = re.search(search_str, text)
    if match:
        return match.group().split('[')[-1].strip(']')


def get_cat(text: str, path_to_meta: str):
    """parse the category from text, if fail, lookup in meta data file (slow) and return the primary category"""
    cat = cat_parser(text)
    if cat is not None:
        return cat
    else:  # if category can not be parsed from the text, look up in metadata
        cat_list = cat_look_up(path2id(text),path_to_meta)
        cat = cat_list.split(' ')[0]  # get the main category if there are more than one
        return cat

