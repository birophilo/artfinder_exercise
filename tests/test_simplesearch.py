import json

import pytest

from tests.fixtures import TEST_FIXTURES_BASIC, TEST_FIXTURES_ADVANCED
from simplesearch import WordSearcher


def test_build_word_index():
    # unit test for building word index for single text file
    searcher = WordSearcher(test_mode=True)

    with open('tests/word_index_1.json') as f:
        expected_results = json.load(f)

    results = searcher.build_word_index_for_file('tests/directory/file_01.txt')

    assert results == expected_results


def test_get_formatted_word_list():
    # unit test for formatting text, stripping whitespace and punctuation
    searcher = WordSearcher(test_mode=True)

    with open('tests/formatted_word_list_1.json') as f1:
        expected_results = json.load(f1)

    with open('tests/directory/file_01.txt') as f2:
        text = f2.read()

    results = searcher.get_formatted_word_list(text)

    assert results == expected_results


# functional test for variety of text input with expected output
@pytest.mark.parametrize("fixture", TEST_FIXTURES_BASIC)
def test_rank_results_basic(fixture):

    searcher = WordSearcher(test_mode=True)
    results = searcher.handle_input(fixture["input"])

    assert results == fixture["expected"]


# functional test with more advanced ranking system (word match % * total matches)
@pytest.mark.parametrize("fixture", TEST_FIXTURES_ADVANCED)
def test_rank_results_advanced(fixture):

    searcher = WordSearcher(test_mode=True, ranking_system="advanced")
    results = searcher.handle_input(fixture["input"])

    assert results == fixture["expected"]
