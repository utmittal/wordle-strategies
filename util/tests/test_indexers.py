from util.indexers import get_letter_index, get_letter_position_index, get_repeated_letter_position_index


def test_get_letter_index_single_word():
    word_list = ['test']

    letter_index = get_letter_index(word_list)

    assert letter_index == {
        't': {'test'},
        'e': {'test'},
        's': {'test'}
    }


def test_get_letter_index_multiple_words():
    word_list = ['test', 'post']

    letter_index = get_letter_index(word_list)

    assert letter_index == {
        't': {'test', 'post'},
        'e': {'test'},
        's': {'test', 'post'},
        'p': {'post'},
        'o': {'post'}
    }


def test_get_letter_index_words_of_different_lengths():
    word_list = ['test', 'poster']

    letter_index = get_letter_index(word_list)

    assert letter_index == {
        't': {'test', 'poster'},
        'e': {'test', 'poster'},
        's': {'test', 'poster'},
        'p': {'poster'},
        'o': {'poster'},
        'r': {'poster'}
    }


def test_get_letter_position_index_single_word():
    word_list = ['test']

    letter_index = get_letter_position_index(word_list)

    assert letter_index == {
        't': {
            0: {'test'},
            3: {'test'}
        },
        'e': {
            1: {'test'}
        },
        's': {
            2: {'test'}
        }
    }


def test_get_letter_position_index_multiple_words():
    word_list = ['test', 'post']

    letter_index = get_letter_position_index(word_list)

    assert letter_index == {
        't': {
            0: {'test'},
            3: {'test', 'post'}
        },
        'e': {
            1: {'test'}
        },
        's': {
            2: {'test', 'post'}
        },
        'p': {
            0: {'post'}
        },
        'o': {
            1: {'post'}
        }
    }


def test_get_letter_position_index_words_of_different_length():
    word_list = ['test', 'poster']

    letter_index = get_letter_position_index(word_list)

    assert letter_index == {
        't': {
            0: {'test'},
            3: {'test', 'poster'}
        },
        'e': {
            1: {'test'},
            4: {'poster'}
        },
        's': {
            2: {'test', 'poster'}
        },
        'p': {
            0: {'poster'}
        },
        'o': {
            1: {'poster'}
        },
        'r': {
            5: {'poster'}
        }
    }


def test_get_repeated_letter_position_index_no_repeated_letters_returns_empty_index():
    word_list = ['post']

    letter_index = get_repeated_letter_position_index(word_list)

    assert letter_index == {}


def test_get_repeated_letter_position_index_single_word_with_double_letter():
    word_list = ['test']

    letter_index = get_repeated_letter_position_index(word_list)

    assert letter_index == {
        't': {
            (0, 3): {'test'}
        }
    }


def test_get_repeated_letter_position_index_single_word_with_more_than_two_letters():
    word_list = ['eevee']

    letter_index = get_repeated_letter_position_index(word_list)

    assert letter_index == {
        'e': {
            (0, 1): {'eevee'},
            (0, 1, 3): {'eevee'},
            (0, 1, 3, 4): {'eevee'},
            (0, 1, 4): {'eevee'},
            (0, 3): {'eevee'},
            (0, 3, 4): {'eevee'},
            (0, 4): {'eevee'},
            (1, 3): {'eevee'},
            (1, 3, 4): {'eevee'},
            (1, 4): {'eevee'},
            (3, 4): {'eevee'}
        }
    }


def test_get_repeated_letter_position_index_multiple_words_with_varying_letters():
    word_list = ['test', 'eevee', 'ozone']

    letter_index = get_repeated_letter_position_index(word_list)

    assert letter_index == {
        'e': {
            (0, 1): {'eevee'},
            (0, 1, 3): {'eevee'},
            (0, 1, 3, 4): {'eevee'},
            (0, 1, 4): {'eevee'},
            (0, 3): {'eevee'},
            (0, 3, 4): {'eevee'},
            (0, 4): {'eevee'},
            (1, 3): {'eevee'},
            (1, 3, 4): {'eevee'},
            (1, 4): {'eevee'},
            (3, 4): {'eevee'}
        },
        'o': {
            (0, 2): {'ozone'}
        },
        't': {
            (0, 3): {'test'}
        }
    }


def test_get_repeated_letter_position_index_multiple_words_with_same_indices():
    word_list = ['root', 'boot', 'hoot']

    letter_index = get_repeated_letter_position_index(word_list)

    assert letter_index == {
        'o': {
            (1, 2): {'root', 'boot', 'hoot'}
        }
    }
