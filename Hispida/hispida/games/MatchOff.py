import random, json, sys
from time import time
from datetime import datetime
from collections import defaultdict
from hispida.utils.ProgressBar import ProgressBar
from hispida.utils.TimeFormat import format_time, get_time
from Grid import Grid
from hispida.bots.MinmaxBot import MinmaxBot

STANDARD_NR_OF_GAMES = 3
MATCH_OFF_FOLDER = "../../docs/match_offs/"

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


def _print_end_score_to_console(victories: dict, timestamp):
    print("{} games played.\n".format(len(victories['games'])))
    print("End score:\n")
    victories_json = json.dumps(victories, indent=4)
    print(victories_json)
    print("\nDuration: " + format_time(timestamp))


def _print_end_score_to_file(victories: dict, timestamp, print_folder):
    victors = list(victories.keys())
    victor_names = [bot.__class__.__name__ for bot in victors if type(bot) != str]
    file_name = print_folder + victor_names[0] + "_vs_" + victor_names[1] + "@" + get_time() + ".txt"

    writer = open(file_name, 'w')
    writer.write(str(STANDARD_NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for index in range(len(victors)):
        writer.write(_get_class_name_player(victors[index]) + " : " + str(victories.get(victors[index])) + "\n")

    writer.write("\nDuration: " + format_time(timestamp) + "\n")

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

    i, progress = 0, ProgressBar()
    while not grid.game_over() and not grid.is_full():
        progress.next()
        i = (i + 1) % 2
        start, column, end = time(), players[i].choose_move(grid), time()
        with open(MATCH_OFF_FOLDER + "times.txt", 'a') as writer:
            writer.write("{} : {}\n".format(players[i], end - start))
        grid.add_pawn(column, players[i].bot_id)
    progress.end()

    return _game_result(bots, grid)


def _run_games(nr_of_games, bots) -> list:
    game_results, score_board = [], defaultdict(int)
    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write('{:3}'.format('#{}'.format(i + 1)))

        game_result = _run_one_game(bots)

        game_results.append(game_result)
        bot = _get_bot_from_id(bots, game_result['winner'])
        score_board[bot] += 1
    return game_results


def _find_end_scores_winners(scores):
    highest_score = max(scores.values())

    return [score for score in scores if scores[score] == highest_score]


def _calc_test_end_scores(game_results, bots):
    scores = {
        'X': 0,
        'O': 0,
        'exaequo': 0
    }
    for game_result in game_results:
        scores[game_result['winner']] += 1

    # TODO re-write next line
    scores['winners'] = [_get_full_bot_description_from_id(bots, bot_id) for bot_id in _find_end_scores_winners(scores)]

    return scores


def _test_result(game_results, bots, duration) -> dict:
    return {
        'bots':
            [{
                'id': bot.bot_id,
                'class': bot.__class__.__name__,
                'configuration': bot.get_configuration()
            } for bot in bots],
        'duration': format_time(duration),
        'games': game_results,
        'end_scores': _calc_test_end_scores(game_results, bots)
    }


def _run_test(bots, nr_of_games) -> dict:
    """1 test (with bot-config-pair) = m games"""

    start, game_results = datetime.now().timestamp(), _run_games(nr_of_games, bots)
    test_duration = datetime.now().timestamp() - start

    test_json = _test_result(game_results, bots, test_duration)
    _print_end_score_to_console(test_json, test_duration)
    return test_json


def _get_description_winner(winner: dict) -> str:
    if winner == 'exaequo':
        return 'exaequo'
    return winner['class'] + ":" + str(winner['configuration'])


def _print_to_file(file_name, json_file):
    with open(file_name, 'w') as writer:
        writer.write(str(json_file))


def _calculate_where_left_off(file_name) -> int:
    try:
        with open(file_name, 'r') as reader:
            return reader.read().count("\n")
    except FileNotFoundError:
        return 0


def match_off(bots, file_name="match_off.json", nr_of_games=30):
    """The given bots participate in a round-robin tournament to determine a ranking."""
    test_number, total_number_of_tests = 0, len(bots) / 2 * (len(bots) - 1)
    left_off_line = _calculate_where_left_off(MATCH_OFF_FOLDER + file_name)
    for i, bot_i in enumerate(bots):
        test_results = []
        for bot_j in bots[i + 1:]:
            test_number += 1
            if test_number < left_off_line:
                continue
            sys.stdout.write("TEST {}/{}\n".format(test_number, int(total_number_of_tests)))
            bot_i.bot_id, bot_j.bot_id = 'X', 'O'
            test_results.append(_run_test((bot_i, bot_j), nr_of_games=nr_of_games))

        if test_results:
            # save test results. 1 line per test result. TODO re-write this because messy.
            with open(MATCH_OFF_FOLDER + file_name, 'a') as writer:
                writer.write("\n{}".format(test_results))

    # TODO transform separate results in one json
    _match_off_results(file_name)


def _competing_bots():
    bots = []
    for i in range(-2, 0):
        for j in range(-2, 0):
            bots.append(MinmaxBot('Z', heuristic_bot=i, heuristic_opponent=j))
    return bots


# TODO make schema of final json output, e.g.: time, winner, ranking, matches
def _match_off_results(test_results, start_time) -> dict:
    return {
        'time': start_time,
        'tests': test_results,
        'end_scores': _calc_match_off_end_scores(test_results)
    }


def _calc_match_off_end_scores(test_results):
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


#
# ULTIMATE MATCH OFF TODO: maybe move in different file
#

def ultimate_match_off():
    """Define here the bots you want to test against each other. Use then the function match_off."""
    bots, file_name = _competing_bots(), "test_1.txt"
    start_time = datetime.now().isoformat()

    match_off(bots, file_name=file_name, nr_of_games=2)

    with open(MATCH_OFF_FOLDER + file_name, 'r') as reader:
        st = reader.read().replace("\'", "\"").replace("\n", "")
        test_results = json.loads(st)
    sys.stdout.write("\n\nRound-robin match-off done.")
    results_json = json.dumps(_match_off_results(test_results, start_time), indent=4)
    _print_to_file(MATCH_OFF_FOLDER + file_name, results_json)


ultimate_match_off()
