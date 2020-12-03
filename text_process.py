import nltk
nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def raw_count(jargon: str, text: str)-> int:
    """ return number of occurent of a jargon in str content of an article"""
    # split text into words
    tokens = word_tokenize(text)

    # remove words that are less than 2 characters
    tokens = [tok for tok in tokens if len(tok)>2]

    # remove tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # filter out stop words (which is all lower case)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # bag of words for this document: a dictionary of word: number of counts
    bow = Counter(tokens)
    
    return bow[jargon.lower()]

