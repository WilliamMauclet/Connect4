import os
import sys

sys.path.insert(0, os.path.abspath("."))

import random
import json
import time
from time import localtime
from datetime import datetime
from hispida.utils import ProgressBar

from Grid import Grid
from hispida.bots.MinmaxBot import MinmaxBot

STANDARD_NR_OF_GAMES = 3
TEST_ROUND_RESULTS_FOLDER = "test_round_results/"

"""
    HIERARCHY
    ---------
    
    MATCH-OFF   = Lots of Bots against one another in a round-robin tournament
                = nr_bots*(nr_bots - 1)/2 matches
    MATCH       = 2 Bots facing off against each other
                = default 30 games
    GAME        = 1 game
                = max 42 moves
"""


# TODO wtf is test round?
def _get_bot_from_id(bots, bot_id: str):
    if bot_id == 'exaequo':
        return 'exaequo'
    for bot in bots:
        if bot.bot_id == bot_id:
            return bot


def _get_full_bot_description_from_id(bots, bot_id: str):
    if bot_id == 'exaequo':
        return 'exaequo'
    for bot in bots:
        if bot.bot_id == bot_id:
            return {
                'class': bot.__class__.__name__,
                'configuration': bot.get_configuration()
            }


def _get_class_name_player(player):
    if player == 'exaequo':
        return player
    else:
        return player.__class__.__name__


# TODO put time formatters in utils class
def _format_time(timestamp):
    hours = timestamp // 3600
    minutes = (timestamp % 3600) // 60
    seconds = (timestamp % 60) // 1
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s\n"


def _get_time():
    time_string = str(localtime()[1]) + "M" + \
                  str(localtime()[2]) + "D_" + \
                  str(localtime()[3]) + "h" + \
                  str(localtime()[4]) + "m"
    return time_string


def _print_end_score_to_console(victories: dict, timestamp):
    print(len(victories['games']) + " games played.\n")
    print("End score:\n")
    victories_json = json.dumps(victories, indent=4)
    print(victories_json)
    print("\nDuration: " + _format_time(timestamp))


def _print_end_score_to_file(victories: dict, timestamp, print_folder):
    victors = list(victories.keys())
    victor_names = [bot.__class__.__name__ for bot in victors if type(bot) != str]
    file_name = print_folder + victor_names[0] + "_vs_" + victor_names[1] + "@" + _get_time() + ".txt"

    writer = open(file_name, 'w')
    writer.write(str(STANDARD_NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for index in range(len(victors)):
        writer.write(_get_class_name_player(victors[index]) + " : " + str(victories.get(victors[index])) + "\n")

    writer.write("\nDuration: " + _format_time(timestamp) + "\n")

    writer.write("Additional details bots:\n")
    for index in range(len(victors)):
        if victors[index] != 'exaequo':
            writer.write(
                _get_class_name_player(victors[index]) + " : " + str(victors[index].get_configuration() + "\n"))
    writer.close()


def _game_result(bots, grid) -> dict:
    game_result = {}
    winner = _get_bot_from_id(bots, grid.game_over())
    if type(winner) == str:
        game_result['winner'] = winner
    else:
        game_result['winner'] = winner.bot_id
    game_result['end_configuration'] = grid.get_state_string_representation()
    return game_result


def _run_one_game(bots) -> dict:
    grid = Grid()
    players = [bot for bot in bots]  # clone
    random.shuffle(players)

    progress = ProgressBar()
    progress.next()
    i = 0
    while grid.game_over() == -1 and grid.get_free_columns() != []:
        i = (i + 1) % 2
        start = time.time()
        column = players[i].choose_move(grid)
        end = time.time()
        with open("test_round_results/times.txt", 'a') as writer:
            writer.write(str(players[i]) + " : " + str(end - start) + "\n")
        grid.add_pawn(column, players[i].bot_id)
        progress.next()
    progress.end()

    return _game_result(bots, grid)


def _run_games(nr_of_games, bots) -> list:
    game_results = []
    # TODO rename victories_dict?
    victories_dict = {'exaequo': 0}
    for bot in bots:
        victories_dict[bot] = 0

    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write("#" + str(i + 1) + " " * (4 - len(str(i + 1))))

        game_results.append(_run_one_game(bots))

        victor_id = game_results[-1]['winner']
        bot = _get_bot_from_id(bots, victor_id)
        victories_dict[bot] = victories_dict[bot] + 1
    return game_results


def _find_end_scores_winners(scores):
    highest_score = max(scores.values())

    return [score for score in scores if scores[score] == highest_score]


def _calculate_end_scores(game_results, bots):
    scores = {
        'X': 0,
        'O': 0,
        'exaequo': 0
    }
    for game_result in game_results:
        scores[game_result['winner']] += 1

    scores['winner'] = [_get_full_bot_description_from_id(bots, id) for id in _find_end_scores_winners(scores)]

    return scores


def _test_result(game_results, bots, duration) -> dict:
    return {
        'bots':
            [{
                'id': bot.bot_id,
                'class': bot.__class__.__name__,
                'configuration': bot.get_configuration()
            } for bot in bots],
        'duration': _format_time(duration),
        'game': game_results,
        'end_scores': _calculate_end_scores(game_results, bots)
    }


def _run_test(bots, nr_of_games) -> dict:
    # 1 test (with bot-config-pair) = m games

    start = datetime.now().timestamp()
    # TODO make run_games return (start, game_results, end) !!
    game_results = _run_games(nr_of_games, bots)
    end = datetime.now().timestamp()

    test_duration = end - start

    test_json = _test_result(game_results, bots, test_duration)

    _print_end_score_to_console(test_json, test_duration)

    # test_result = test_result(game_results, bots, end_scores, test_duration)

    # for victor in game_results:
    #    test_result['end_scores'][victor] = game_results['victor']

    return test_json


def _calc_test_round_end_scores(test_results):
    # TODO re-use find_end_scores_winners?
    scores = {}

    for test_result in test_results:
        winners = test_result['end_scores']['winner']

        for winner in winners:
            desc_winner = _get_description_winner(winner)
            if desc_winner in scores:
                scores[desc_winner] += 1
            else:
                scores[desc_winner] = 1

    import operator
    return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    #  'scores': scores,
    #  'ranking': sorted(scores, key= lambda score: scores[score])


def _get_description_winner(winner: dict) -> str:
    if winner == 'exaequo':
        return 'exaequo'
    return winner['class'] + ":" + str(winner['configuration'])


# 1 test -> n games
def _test_round_result(test_results, start_time) -> dict:
    return {
        'time': start_time,
        'tests': test_results,
        'end_scores': _calc_test_round_end_scores(test_results)
    }


def _print_to_file(file_name, json):
    with open(file_name, 'w') as writer:
        writer.write(str(json))


def run_test_test_round():
    dependent_variable, independent_variable = MinmaxBot('X'), MinmaxBot('O')

    start_time = datetime.now().timestamp()
    test_results = []

    for heuristic_bot in range(2, 3):
        for heuristic_opponent in range(1, 2):
            dependent_variable.set_heuristic_params(heuristic_bot=heuristic_bot,
                                                    heuristic_opponent=heuristic_opponent)
            independent_variable.set_heuristic_params(heuristic_bot=heuristic_bot,
                                                      heuristic_opponent=heuristic_opponent)
            test_results.append(_run_test((independent_variable, dependent_variable), nr_of_games=30))

    sys.stdout.write("\n\nMultiple tests done.")
    file_name = "test_round_results/test_test_round.json"
    results_json = json.dumps(_test_round_result(test_results, start_time), indent=4)
    _print_to_file(file_name, results_json)


def _calculate_where_left_off(file_name) -> int:
    try:
        with open(file_name, 'r') as reader:
            return reader.read().count("\n")
    except FileNotFoundError:
        return 0


# STRUCTURE
# 1 test round = n tests
# 1 test = 2 bots with configs = m games
def run_test_round(file_name="TODO_RENAME.json"):
    """1 test round = n tests (each with bot-config-pair) = n*m games"""
    # TODO test should resume where left off. => user calculate_Where_left_off NOT YET IMPLEMENTED !!!!!!!!!!!!!
    # e.g. count nr of lines in file and calculate modulo first range

    from hispida.bots import MinmaxBot
    independent_variable = MinmaxBot('O')
    dependent_variable = MinmaxBot('X')

    start_time = datetime.now().isoformat()

    # TODO: refactor how to say how far along (cf. ProgressBar)
    heuristic_bot_range, heuristic_opponent_range = range(-2, 3), range(-2, 3)
    total_number_of_tests = len(heuristic_bot_range) * len(heuristic_opponent_range)
    test_number, test_results = 0, []
    left_off_line = _calculate_where_left_off(TEST_ROUND_RESULTS_FOLDER + file_name)
    for heuristic_bot in heuristic_bot_range:
        for heuristic_opponent in heuristic_opponent_range:
            test_number += 1
            if test_number < left_off_line:
                continue

            _run_test_round_test(dependent_variable, file_name, heuristic_opponent, heuristic_bot,
                                 independent_variable, test_number, test_results, total_number_of_tests)

    with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'r') as reader:
        st = reader.read().replace("\'", "\"").replace("\n", "")
        test_results = json.loads(st)
    sys.stdout.write("\n\nMultiple tests done.")
    results_json = json.dumps(_test_round_result(test_results, start_time), indent=4)
    _print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)


def _run_test_round_test(dependent_variable, file_name, heuristic_opponent, heuristic_bot, independent_variable,
                         test_number, test_results, total_number_of_tests):
    sys.stdout.write("TEST " + str(test_number) + "/" + str(total_number_of_tests) + "\n")
    dependent_variable.set_heuristic_params(heuristic_bot=heuristic_bot,
                                            heuristic_opponent=heuristic_opponent)
    new_test_result = _run_test((independent_variable, dependent_variable), nr_of_games=30)
    test_results.append(new_test_result)
    # temporary save
    with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'a') as writer:
        writer.write(str(test_results).replace("{'bots'", "\n{'bots'"))  # 1 line per test result


def match_off(bots, file_name="match_off.json", nr_of_games=30):
    """The given bots participate in a round-robin tournament to determine a ranking."""
    total_number_of_tests = len(bots) / 2 * (len(bots) - 1)
    test_number, test_results = 0, []
    left_off_line = _calculate_where_left_off(TEST_ROUND_RESULTS_FOLDER + file_name)
    for i in range(len(bots)):
        for j in range(i + 1, len(bots)):
            test_number += 1
            if test_number < left_off_line:
                continue
            sys.stdout.write("TEST " + str(test_number) + "/" + str(total_number_of_tests) + "\n")
            bots[i].bot_id, bots[j].bot_id = 'X', 'O'
            test_results.append(_run_test((bots[i], bots[j]), nr_of_games=nr_of_games))
        # temporary save of match-off
        with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'a') as writer:
            writer.write(str(test_results).replace("{'bots'", "\n{'bots'"))  # 1 line per test result
            # TODO re-write this because messy.


def _match_off_test_round():
    """Define here the bots you want to test against each other. Use then the function match_off."""
    bots, file_name, start_time = \
        _competing_bots(), \
        "test_" + str(_get_and_increment_test_number), \
        datetime.now().isoformat()

    match_off(bots, file_name=file_name)

    with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'r') as reader:
        st = reader.read().replace("\'", "\"").replace("\n", "")
        test_results = json.loads(st)
    sys.stdout.write("\n\nRound-robin match-off done.")
    results_json = json.dumps(_test_round_result(test_results, start_time), indent=4)
    _print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)


def _competing_bots():
    bots = []
    for i in range(-2, -1):
        for j in range(-2, -1):
            bots.append(MinmaxBot('Z', heuristic_bot=i, heuristic_opponent=j))
    return bots


def _get_and_increment_test_number() -> int:
    with open(TEST_ROUND_RESULTS_FOLDER + "test_nr.txt", 'rw') as reader_writer:
        test_number = int(reader_writer.read())
        reader_writer.write(str(test_number + 1))
        return test_number


# run_test_round_A()
# run_test_test_round()
# run_test_round()
_match_off_test_round()
