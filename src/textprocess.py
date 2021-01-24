import string
import codecs
import re
import json
from typing import List

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
import nltk
nltk.download('punkt')
nltk.download('stopwords')


# copy from https://github.com/quynhneo/detm-arxiv/blob/master/arxivtools/preprocessing.py
def preprocess(document: str) -> List[str]:
    """
    INPUT: a string
    OUTPUT: a list of token
        tokenize, lower case,
        remove punctuations: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', and new line character
        remove words with less than 1 characters from document
        remove stopwords
    note:
        pure numerics are allowed, in case searching for 3D in "3 D"
        single characters are allowed

    """
    result = []

    # replace punctuation with white space
    document = document.lower().replace("’", " ").replace("'", " ").replace("\n", " ").translate(
        str.maketrans(string.punctuation, " "*len(string.punctuation)))

    for token in document.split():
        #if len(token) > 1 and token not in stopwords and token.islower():
            # token.islower() return False for pure numeric
        result.append(token)

    return result


def term_freq(jargon: str, text: str) -> int:
    """ return number of occurrence of a jargon in str content of an article
        subscripts, number, non-alphabetic, stopwords are ignored
    """
    # convert \\n to \n in text so tokenizer knows to split
    text = codecs.decode(text, 'unicode_escape') #

    # split text into words
    tokens = word_tokenize(text)

    # remove words that are less than 2 characters
    # tokens = [tok for tok in tokens if len(tok)>2] # remove this, some jargons may be short abbreviation

    # remove tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # filter out stop words (which is all lower case)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # bag of words for this document: a dictionary of word: number of counts
    # bow = Counter(tokens) # then return bow[jargon.lower()]

    return tokens.count(jargon.lower()) # only count the word of interest


def phrase_count(phrase: List[str], tokens: List[str], similarity=80) -> int:
    """count the number of occurrence of phrases a tokenized document
    both phrase and tokens must be list of words and have been cleaned by preprocess
    similarity: min levenshtein similarity ratio to accept a match
     """

    count = 0
    len_phrase = len(phrase)

    for i in range(len(tokens)-len_phrase+1):
        ngram = ""
        j = 0
        for j in range(i, i+len_phrase):
            ngram = ngram+" "+tokens[j]
        ngram.strip()
        if not ngram == "":
            if fuzz.ratio(ngram, " ".join(phrase)) > similarity:
                print([ngram, phrase, i, j, fuzz.ratio(ngram, " ".join(phrase)) ])
                count = count + 1
    return count


def terms_freq(jargons_list: List[str], text: str, similarity=80, method: str = 'norm') -> List[int]:
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
        return [phrase_count(preprocess(jargon), tokens, similarity=similarity) for jargon in jargons_list]

    if method == 'bool':
        return [phrase_count(preprocess(jargon), tokens, similarity=similarity) >= 1 for jargon in jargons_list]

    if method == 'norm':
        return [phrase_count(preprocess(jargon), tokens, similarity=similarity)/len(tokens) for jargon in jargons_list]

    raise Exception  # if no method exist


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

