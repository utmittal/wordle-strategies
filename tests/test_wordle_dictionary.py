import random
from pathlib import Path

from util.project_path import project_path
from wordle_dictionary import WordleDictionary


def test_get_random_puzzle_returns_word_in_puzzle_list():
    puzzle_list = __get_valid_puzzles()
    wd = WordleDictionary()

    random_puzzle = wd.get_random_puzzle()

    assert random_puzzle in puzzle_list


def test_get_all_puzzles_returns_whole_puzzle_list():
    puzzle_list = __get_valid_puzzles()
    wd = WordleDictionary()

    all_puzzles = wd.get_all_puzzles()

    assert all_puzzles == puzzle_list


def test_get_all_words_returns_whole_word_list():
    word_list = __get_valid_guesses()
    wd = WordleDictionary()

    all_words = wd.get_all_words()

    assert all_words == word_list


def test_contains_returns_true_for_word_from_puzzle_list():
    random_puzzle_word = random.choice(__get_valid_puzzles())
    wd = WordleDictionary()

    assert wd.contains(random_puzzle_word) == True


def test_contains_returns_true_for_word_from_guesses_list():
    random_guess_word = random.choice(__get_valid_guesses())
    wd = WordleDictionary()

    assert wd.contains(random_guess_word) == True


def test_contains_returns_false_for_invalid_word():
    invalid_word = "DEFINITELY_INVALID_WORD"
    wd = WordleDictionary()

    assert wd.contains(invalid_word) == False


def test_contains_works_with_lowercase_argument():
    random_guess_word = random.choice(__get_valid_guesses()).lower()
    wd = WordleDictionary()

    assert wd.contains(random_guess_word) == True


def test_contains_works_with_uppercase_argument():
    random_guess_word = random.choice(__get_valid_guesses()).upper()
    wd = WordleDictionary()

    assert wd.contains(random_guess_word) == True


def test_get_random_word_returns_word_in_guesses_list():
    guesses_list = __get_valid_guesses()
    wd = WordleDictionary()

    random_word = wd.get_random_word()

    assert random_word in guesses_list


def test_get_filtered_guesses_returns_all_valid_guesses_when_given_empty_arguments():
    guesses_list = set(__get_valid_guesses())
    wd = WordleDictionary()

    filtered_guesses = wd.get_filtered_guesses_v3([], {}, {}, set())

    assert filtered_guesses == guesses_list


# TODO: Add more tests for get_filtered_guesses

def __get_valid_puzzles() -> list[str]:
    return __parse_words_from_file('database/valid_puzzles.txt')


def __get_valid_guesses() -> list[str]:
    return __parse_words_from_file('database/valid_guesses.txt')


def __parse_words_from_file(path: Path | str) -> list[str]:
    path = project_path(path)
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return [w.strip().upper() for w in lines]
