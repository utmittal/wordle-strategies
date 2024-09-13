import random

from player_interface import Player
from game_simulator import LetterState, TOTAL_LETTERS, GameState


class PlayerLogicalGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word that
    satisfies all the information it has learned so far. I.e. it will consider the position of yellows when making its
    guesses.
    """
    __name = "LogicalGuesser"

    def __init__(self, wd, debug=False):
        self.__wd = wd
        self.__debug = debug
        self.__greens = []
        self.__greys = set()
        self.__yellows = {}

    @staticmethod
    def get_name():
        return PlayerLogicalGuesser.__name

    def get_next_guess(self, game_state: GameState, turn):
        if turn == 0:
            return self.__wd.get_random()

        self.__update_known_info(game_state, turn)
        possible_guesses = self.__wd.get_filtered_guesses_v2(greens=self.__greens, yellows=self.__yellows,
                                                             greys=self.__greys)

        if self.__debug:
            print("Greens - " + str(self.__greens) + " | Yellows - " + str(self.__yellows) + " | Excludes - " + str(
                self.__greys))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(list(possible_guesses))

    def __update_known_info(self, game_state: GameState, turn):
        current_yellows = []
        current_greens = []
        new_greys = set()

        # evaluate current row
        for game_letter, i in zip(game_state.get_last_turn(), range(TOTAL_LETTERS)):
            if game_letter.color == LetterState.grey:
                new_greys.add(game_letter.letter)
            elif game_letter.color == LetterState.green:
                current_greens.append((game_letter.letter, i))
            elif game_letter.color == LetterState.yellow:
                current_yellows.append(game_letter.letter)
            else:
                raise Exception("Something has gone very wrong.")

        # We need this to handle the corner case where a double letter in a guess results in a yellow and grey.
        # If the letter is in yellow, we don't want to put it in grey.
        for ne in new_greys:
            if ne not in current_yellows and ne not in [t[0] for t in current_greens]:
                self.__greys.add(ne)

        self.__greens = current_greens

        # Note: the logic below doesn't handle repeated yellows. Handling repeated letters properly might further
        # reduce the logical set of options available to us.
        self.__yellows = {}
        for inc in current_yellows:
            self.__yellows[inc] = [0, 1, 2, 3, 4]
        for row in game_state[:turn]:
            for game_letter, i in zip(row, range(TOTAL_LETTERS)):
                if game_letter.letter in current_yellows and (
                        game_letter.color == LetterState.yellow or game_letter.color == LetterState.green):
                    if i in self.__yellows[game_letter.letter]:
                        self.__yellows[game_letter.letter].remove(i)
