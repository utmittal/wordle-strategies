import random
from collections import Counter

from players.player_interface import Player
from game_simulator import LetterState, TOTAL_LETTERS, GameState
from wordle_dictionary import WordleDictionary


class PlayerAdieuStarter(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word that
    satisfies all the information it has learned so far. I.e. it will consider the position of yellows when making its
    guesses.
    """
    __name = "AdieuStarter"

    def __init__(self, wd: WordleDictionary, debug: bool = False):
        self.__wd = wd
        self.__debug = debug
        self.__greens = []
        self.__greys = set()
        self.__single_yellows = {}
        self.__double_yellows = {}

    @staticmethod
    def get_name() -> str:
        return PlayerAdieuStarter.__name

    def get_next_guess(self, game_state: GameState, turn: int) -> str:
        if turn == 0:
            return "ADIEU"

        self.__update_known_info(game_state, turn)
        possible_guesses = self.__wd.get_filtered_guesses_v3(greens=self.__greens, single_yellows=self.__single_yellows,
                                                             double_yellows=self.__double_yellows,
                                                             greys=self.__greys)

        if self.__debug:
            print("Greens - " + str(self.__greens) + " | Yellows - " + str(
                self.__single_yellows) + " | Excludes - " + str(
                self.__greys))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(list(possible_guesses))

    def __update_known_info(self, game_state: GameState, turn: int):
        current_yellows = []
        current_greens = []
        new_greys = []

        # evaluate current row
        for game_letter, i in zip(game_state.get_last_turn(), range(TOTAL_LETTERS)):
            if game_letter.color == LetterState.grey:
                new_greys.append(game_letter.letter)
            elif game_letter.color == LetterState.green:
                current_greens.append((game_letter.letter, i))
            elif game_letter.color == LetterState.yellow:
                current_yellows.append(game_letter.letter)
            else:
                raise Exception("Something has gone very wrong.")

        # We need this to handle the corner case where a double letter in a guess results in a yellow and grey.
        # If the letter is in yellow or green, we don't want to put it in grey.
        for ne in new_greys:
            if ne not in current_yellows and ne not in [t[0] for t in current_greens]:
                self.__greys.add(ne)

        self.__greens = current_greens

        self.__single_yellows = {}
        self.__double_yellows = {}
        yellow_counter = Counter(current_yellows)
        for yellow_letter in yellow_counter:
            possible_positions = [0, 1, 2, 3, 4]
            for row in game_state[:turn]:
                for i, game_letter in enumerate(row):
                    if game_letter.letter == yellow_letter:
                        if i in possible_positions:
                            possible_positions.remove(i)

            if yellow_counter[yellow_letter] == 1:
                self.__single_yellows[yellow_letter] = possible_positions
            elif yellow_counter[yellow_letter] == 2:
                self.__double_yellows[yellow_letter] = possible_positions
            else:
                raise Exception(
                    f"Yellow count for {yellow_letter} was {yellow_counter[yellow_letter]} which should be impossible.")
