import nltk
nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs
from typing import List

def term_freq(jargon: str, text: str)-> int:
    """ return number of occurent of a jargon in str content of an article
        subscripts, number, non-alphabetic, stopwords are ignored
    """
    # convert \\n to \n in text so tokenizer knows to split
    text=codecs.decode(text, 'unicode_escape') #

    # split text into words
    tokens = word_tokenize(text)

    # remove words that are less than 2 characters
    #tokens = [tok for tok in tokens if len(tok)>2] # remove this, some jargons may be short abbreviation

    # remove tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # filter out stop words (which is all lower case)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # bag of words for this document: a dictionary of word: number of counts
    #bow = Counter(tokens) # then return bow[jargon.lower()]
    
    return tokens.count(jargon.lower()) # only count the word of interest

def terms_freq(jargons_list: List[str], text: str, method: str)-> List[int]:
    """ for each jargon in jargon lists, return a number of its occurence in str content of text.
        both jargons and text are converted to lower case before counting
        methods: 
            raw: raw count
            bool: False for raw count = 0, True for >= 1
            norm: raw count/ processed text length  
        subscripts, number, non-alphabetic, stopwords can't be used in norm method 
    """
    # apply minimal processing for raw count
    text = codecs.decode(text, 'unicode_escape') # convert \\n to \n in text so tokenizer knows to split 
    tokens = word_tokenize(text) # split text into words
    tokens = [w.lower() for w in tokens]  # convert to lower case
    if method == 'raw': # raw count
        return [tokens.count(jargon.lower()) for jargon in jargons_list]
    if method == 'bool':
        return [tokens.count(jargon.lower()) >= 1 for jargon in jargons_list]
    tokens = [word for word in tokens if word.isalpha()] # remove tokens that are not alphabetic
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]  # filter out stop words (which is all lower case)
    if method == 'norm':
        return [tokens.count(jargon.lower())/len(tokens) for jargon in jargons_list]
    raise(Exception) # no method exist   
