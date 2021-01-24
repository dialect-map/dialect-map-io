import pytest
from src.textprocess import phrase_count


def test_phrase_count_1():
    assert(phrase_count("Hello World", ["hello", "world","abc", "def"]) == 1)


def test_phrase_count_2():
    assert(phrase_count("Hello World", ["hello", "world","physics", "hello", "world"]) == 2)


def test_phrase_count_3():
    assert(phrase_count("Hello World", ["hello-world", "hello", "world"]) == 2)
