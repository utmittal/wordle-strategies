from itertools import combinations


def get_letter_index(words: list[str] | set[str] | tuple[str]) -> dict[str, set[str]]:
    # create index of words containing a specific letter
    letter_index = {}
    for word in words:
        letters = list(word)
        for l in letters:
            if l in letter_index:
                letter_index[l].add(word)
            else:
                letter_index[l] = {word}

    return letter_index


def get_letter_position_index(words: list[str] | set[str] | tuple[str]) -> dict[str, dict[int, set[str]]]:
    letter_pos_index = {}
    for word in words:
        letters = list(word)
        for i, l in enumerate(letters):
            if l not in letter_pos_index:
                letter_pos_index[l] = {i: {word}}
            else:
                letter_dic = letter_pos_index[l]
                if i not in letter_dic:
                    letter_dic[i] = {word}
                else:
                    letter_dic[i].add(word)

    return letter_pos_index


def get_repeated_letter_position_index(words: list[str] | set[str] | tuple[str]) -> dict[
    str, dict[tuple[int, ...], set[str]]]:
    # create index of double letters
    repeated_letter_pos_index = {}
    for word in words:
        duplicates = set()
        seen = set()
        for letter in word:
            if letter not in seen:
                seen.add(letter)
            else:
                duplicates.add(letter)

        for d in duplicates:
            positions = sorted([i for i, letter in enumerate(word) if letter == d])
            dupe_count = len(positions)
            for indice_length in range(2, dupe_count + 1):
                indice_tuples = combinations(positions, indice_length)
                for tup in indice_tuples:
                    if d not in repeated_letter_pos_index:
                        repeated_letter_pos_index[d] = {tup: {word}}
                    else:
                        letter_dic = repeated_letter_pos_index[d]
                        if tup not in letter_dic:
                            letter_dic[tup] = {word}
                        else:
                            letter_dic[tup].add(word)

    return repeated_letter_pos_index
