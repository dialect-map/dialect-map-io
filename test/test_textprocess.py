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
    assert(phrase_count(["shello"], ["hello", "world", "physics", "shellos", "world"]) == 2)


def test_terms_freq_1():
    assert(terms_freq(["hello world"], "good morning hello world I am a pre-Process document 1234", method="raw") == [1])


def test_terms_freq_2():
    assert(terms_freq(["hello-world"], "good morning hello world I am a pre-Process document 1234",method= "raw") == [1])


def test_terms_freq_3():
    assert(terms_freq(["hello-world"], "good morning Hello worlD I am a pre-Process document 1234",method= "raw") == [1])


def test_terms_freq_4():
    assert(terms_freq(["hello-world","document"], "good morning Hello"
                                                  " worlD I am a pre-Process document 1234 document",method= "raw") == [1,2])


def test_terms_freq_5():
    assert(terms_freq(["say hello-world","document","arxiv"], "good morning SAY Hello"
                                                  " worlD I am a pre-Process document 1234 document", method="raw") == [2,2,0])


def test_terms_freq_6():
    assert(terms_freq(["say hello-world","document","arxiv"], "good morning SAY Hello"
                                                  " worlD I am a pre-Process document 1234 document", method="bool") == [1,1,0])


def test_terms_freq_6():
    assert(terms_freq([
        "say hello-world","document","arxiv"],
        "good morning SAY Hello  worlD I am a pre-Process document 1234 document",
        method="norm") == [pytest.approx(float(2/13),0.1),pytest.approx(float(2/13),0.1),0])
