import csv
import os.path
from datetime import datetime

from game_simulator import GameSimulator, State
from player_random_guess import PlayerRandomGuesser
from pycharm_termcolor import cprint
from wordle_dictionary import WordleDictionary

from collections import OrderedDict


def play_game(player, provided_puzzle=None, debug=False):
    gs = GameSimulator()
    if provided_puzzle:
        game_state = gs.start_game_with_puzzle(provided_puzzle)
    else:
        game_state = gs.start_game()

    if debug:
        puzzle_word = gs._debug_get_puzzle_word()
        cprint("Puzzle Word - " + puzzle_word.upper(), 'blue')
        print()

    turn = 1
    while gs.is_won() != True and gs.is_lost() != True:
        if debug:
            cprint("Turn " + str(turn), 'red')

        player_guess = player.get_next_guess(game_state)
        game_state = gs.guess(player_guess)

        if debug:
            print("Guess: " + player_guess)
            print("Game State:")
            gs._debug_print_board()

        turn += 1
        if debug:
            inp = input("continue (y)? ")
            if inp != 'y' and inp != '':
                return

    return gs


def evaluate_all_puzzles(player, cycles=1, debug=False):
    total_games = 0
    wins = 0
    losses = 0
    avg_guesses = 0
    win_distribution = [0] * 6
    avg_yellow_greens = [[0] * 3 for _ in range(6)] * 6  # yellows, greens, total_games_in_which_that_row_was_played
    word_freq = [{} for _ in range(6)]  # per row

    wd = WordleDictionary()
    pl = PlayerRandomGuesser()
    puzzle_number = 0
    for cy in range(cycles):
        for new_puzzle in wd.get_all_puzzles():
            if debug:
                puzzle_number += 1
                if puzzle_number % 500 == 0:
                    print("Puzzle Number " + str(puzzle_number))

            # play the game
            gs = play_game(pl, provided_puzzle=new_puzzle)
            if gs.is_won() and gs.is_lost():
                raise Exception("Something has gone very wrong.")

            # gather stats
            total_games += 1

            if gs.is_lost():
                losses += 1

            if gs.is_won():
                wins += 1
                avg_guesses += gs.get_turns()
                win_distribution[gs.get_turns() - 1] += 1

            game_state = gs.get_game_state()
            for row, i in zip(game_state, range(0, 6)):
                # if first element is blank, it means row wasn't played and we no longer need to evaluate
                if row[0][1] == State.blank:
                    break

                yells = 0
                grees = 0

                for elem in row:
                    if elem[1] == State.yellow:
                        yells += 1
                    elif elem[1] == State.green:
                        grees += 1

                avg_yellow_greens[i][0] += yells
                avg_yellow_greens[i][1] += grees
                avg_yellow_greens[i][2] += 1

                guessed_word = ''.join([el[0] for el in row])
                if guessed_word in word_freq[i]:
                    word_freq[i][guessed_word] += 1
                else:
                    word_freq[i][guessed_word] = 1

    # pretty print stats
    cprint("Player:\t\t\t\t\t\t" + pl.get_name(), 'blue')
    cprint("Total Games:\t\t\t\t" + str(total_games), 'blue')
    cprint("Wins:\t\t\t\t\t\t" + str(wins), 'blue')
    cprint("Losses:\t\t\t\t\t\t" + str(losses), 'blue')
    cprint("Win Ratio:\t\t\t\t\t" + "{:.2f}".format(wins / total_games), 'blue')
    cprint("Average Guesses:\t\t\t" + "{:.2f}".format(avg_guesses / wins), 'blue')

    overall_word_freq = {}
    for dic in word_freq:
        for wf in dic:
            if wf in overall_word_freq:
                overall_word_freq[wf] += 1
            else:
                overall_word_freq[wf] = 1
    cprint("Favourite Word:\t\t\t\t" + max(overall_word_freq, key=overall_word_freq.get), 'blue')
    cprint("Least Favourite Word:\t\t" + min(overall_word_freq, key=overall_word_freq.get), 'blue')
    cprint("Favourite Word per row:", 'blue')
    for row, row_no in zip(word_freq, range(1, 7)):
        print("\tRow " + str(row_no) + ":\t\t\t\t" + max(row, key=row.get))

    cprint("\nWin Distribution:", 'blue')
    max_distribution_bar_length = 20
    max_val = max(win_distribution)
    normalized_win_distribution = [round((w / max_val) * max_distribution_bar_length) for w in win_distribution]
    for row, row_no in zip(normalized_win_distribution, range(1, 7)):
        print("\t" + str(row_no) + ": " + str("#" * row))
    cprint("\nAverage Yellows and Greens per row:", 'blue')
    for row, row_no in zip(avg_yellow_greens, range(1, 6)):
        print("\t" + str(row_no) + ": " + "Yellows - " + "{:.2f}".format(
            row[0] / row[2]) + " | Greens - " + "{:.2f}".format(row[1] / row[2]))

    # write results to file
    player_stats = OrderedDict(
        {
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'player_name': pl.get_name(),
            'total_games': total_games,
            'wins': wins,
            'losses': losses,
            'win_ratio': wins / total_games,
            'avg_guesses': avg_guesses / wins,
            'overall_most_used_word': max(overall_word_freq, key=overall_word_freq.get),
            'overall_least_used_word': min(overall_word_freq, key=overall_word_freq.get),
            'most_used_word_row1': max(word_freq[0], key=word_freq[0].get),
            'most_used_word_row2': max(word_freq[1], key=word_freq[1].get),
            'most_used_word_row3': max(word_freq[2], key=word_freq[2].get),
            'most_used_word_row4': max(word_freq[3], key=word_freq[3].get),
            'most_used_word_row5': max(word_freq[4], key=word_freq[4].get),
            'most_used_word_row6': max(word_freq[5], key=word_freq[5].get),
            'win_dist_row1': win_distribution[0],
            'win_dist_row2': win_distribution[1],
            'win_dist_row3': win_distribution[2],
            'win_dist_row4': win_distribution[3],
            'win_dist_row5': win_distribution[4],
            'win_dist_row6': win_distribution[5],
            'avg_row1_yellow': avg_yellow_greens[0][0] / avg_yellow_greens[0][2],
            'avg_row2_yellow': avg_yellow_greens[1][0] / avg_yellow_greens[1][2],
            'avg_row3_yellow': avg_yellow_greens[2][0] / avg_yellow_greens[2][2],
            'avg_row4_yellow': avg_yellow_greens[3][0] / avg_yellow_greens[3][2],
            'avg_row5_yellow': avg_yellow_greens[4][0] / avg_yellow_greens[4][2],
            'avg_row6_yellow': avg_yellow_greens[5][0] / avg_yellow_greens[5][2],
            'avg_row1_green': avg_yellow_greens[0][1] / avg_yellow_greens[0][2],
            'avg_row2_green': avg_yellow_greens[1][1] / avg_yellow_greens[1][2],
            'avg_row3_green': avg_yellow_greens[2][1] / avg_yellow_greens[2][2],
            'avg_row4_green': avg_yellow_greens[3][1] / avg_yellow_greens[3][2],
            'avg_row5_green': avg_yellow_greens[4][1] / avg_yellow_greens[4][2],
            'avg_row6_green': avg_yellow_greens[5][1] / avg_yellow_greens[5][2],
        }
    )

    csv_path = "player_scores/" + pl.get_name() + ".csv"
    if not os.path.exists(csv_path):
        with open(csv_path, 'w+', newline='') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=player_stats.keys())
            writer.writeheader()
    with open(csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=player_stats.keys())
        writer.writerow(player_stats)


# current_player = PlayerRandomGuesser(debug=True)
# play_game(current_player, debug=True)

evaluate_all_puzzles(PlayerRandomGuesser(), cycles=1, debug=True)
