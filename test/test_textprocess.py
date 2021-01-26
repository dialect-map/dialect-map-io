import pytest
from src.textprocess import phrase_count, terms_freq


def test_phrase_count_1():
    assert(phrase_count(["hello", "world"],
                        ["hello", "world", 'this', 'is', 'some',
                         'random', 'text,', 'everything', 'is', 'lower', 'case']) == 1)


def test_phrase_count_2():
    assert(phrase_count(["hello", "world"], ["hello", "world", "physics", "hello", "world"]) == 2)


def test_phrase_count_3():
    assert(phrase_count(["hello", "world"], ["hello",  "hello", "world", "world"]) == 1)


def test_phrase_count_4():
    assert(phrase_count(["hello ","world", "again"], ["hello", "world","again"]) == 1)


def test_phrase_count_5():
    assert(phrase_count(["shello"], ["hello", "world", "physics", "shellos", "world"]) == 1)
    # shellos will match, but not hello


def test_phrase_count_6():
    assert(phrase_count(["say", "hello", "world"],
                        "good morning say hello world I am a pre-Process document 1234 document".split()) == 1)

# term frequency test
def test_terms_freq_1():
    assert(terms_freq(["hello world"], "good morning hello world I am a pre-Process document 1234",
                      method="raw") == [{'jargon': "hello world", 'tf_raw': 1}])


def test_terms_freq_2():
    assert(terms_freq(["hello-world"], "good morning hello world I am a pre-Process document 1234",
                      method= "raw") == [{'jargon': "hello world", 'tf_raw': 1}])


def test_terms_freq_3():
    assert(terms_freq(["hello-world"], "good morning Hello worlD I am a pre-Process document 1234",
                      method= "raw") == [{'jargon': "hello world", 'tf_raw': 1}])


def test_terms_freq_4():
    assert(terms_freq(["hello-world", "document"], "good morning Hello worlD I am a pre-Process document 1234 document",
                      method="raw") == [{'jargon': "hello world", 'tf_raw': 1}, {'jargon': 'document', 'tf_raw': 2}])


def test_terms_freq_5():
    assert(terms_freq(["say hello-world", "document", "arxiv"], "good morning SAY Hello"
                      " worlD I am a pre-Process document 1234 document",
                      method="raw") == [{'jargon': "say hello world", 'tf_raw': 1},
                                        {'jargon': 'document', 'tf_raw': 2},
                                        {'jargon': 'arxiv', 'tf_raw': 0}])


def test_terms_freq_6():
    assert(terms_freq(["say hello-world","document","arxiv"], "good morning SAY Hello"
                                                  " worlD I am a pre-Process document 1234 document",
                      method="bool") == [{'jargon': "say hello world", 'tf_bool': True},
                                        {'jargon': 'document', 'tf_bool': True},
                                        {'jargon':'arxiv','tf_bool': False}])


def test_terms_freq_7():
    assert(terms_freq([
        "say hello-world", "document", "arxiv"],
        "good morning SAY Hello  worlD I am a pre-Process document 1234 document",
        method="norm") == [{'jargon': 'say hello world',
                            'tf_norm': pytest.approx(float(1/13), 0.1)},
                           {'jargon': 'document', 'tf_norm': pytest.approx(float(2/13), 0.1)},
                           {'jargon': 'arxiv', 'tf_norm': 0}])


def test_terms_freq_8():  # when jargon missing space "finetune" or hyphen "kaluzakein: false
    assert(terms_freq([
        "finetune","Contrastive-gradient Learnings"],
        "This is measured by ranking questions based on the cosine similarity of their Grad-CAM\
vectors with that of the reasoning question. We find\
that even top-performing VQA models often rank\
irrelevant questions higher than relevant questions.\
Motivated by this, we introduce a new approach\
called contrastive gradient learning to fine-tune a\
VQA model by adding a loss term that enforces\
relevant sub-questions to be ranked higher than irrelevant questions while answering a reasoning\
question. This is achieved by forcing the cosine\
similarity of the reasoning question's Grad-CAM\
vector with that of a sub-question to be higher than\
with that of an irrelevant question. We find that\
our approach improves the model's consistency, learning Contrastive-gradient",
        method="bool") == [{'jargon': "finetune", 'tf_bool': False},
                                        {'jargon': 'contrastive gradient learnings', 'tf_bool': True}])
