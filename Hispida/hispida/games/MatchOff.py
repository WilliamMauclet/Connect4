import random, json, sys, ast
from time import time
from datetime import datetime
from collections import defaultdict
from hispida.utils.ProgressBar import ProgressBar
from hispida.utils.TimeFormat import format_time
from Grid import Grid

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


def match_off(bots, file_path="../../docs/match_offs/match_off.json", nr_of_games=30):
    """The given bots participate in a round-robin tournament to determine a ranking."""
    match_number, total_number_of_matches = 0, len(bots) * (len(bots) - 1) // 2
    left_off_line = _calculate_where_left_off(file_path)
    for i, bot_i in enumerate(bots):
        match_results = []
        for bot_j in bots[i + 1:]:
            match_number += 1
            if match_number < left_off_line:
                continue
            sys.stdout.write("TEST {}/{}\n".format(match_number, total_number_of_matches))
            bot_i.bot_id, bot_j.bot_id = 'X', 'O'
            match_results.append(_run_match((bot_i, bot_j), nr_of_games=nr_of_games))

        if match_results:
            # save match results. 1 line per match result. TODO re-write this because messy.
            with open(file_path, 'a') as writer:
                writer.write("{}\n".format(match_results))

    # TODO transform separate results in one json
    results = _match_off_results(total_number_of_matches, file_path)
    pass


def _calculate_where_left_off(file_path) -> int:
    try:
        with open(file_path, 'r') as reader:
            return reader.read().count("\n")
    except FileNotFoundError:
        return 0


def _match_off_results(total_number_of_matches, file_path) -> dict:
    matches = []
    with open(file_path, 'r') as reader:
        for _ in range(total_number_of_matches):
            matches.append(ast.literal_eval(reader.readline()))  # un-jsonify? => use ast!

    return {
        'matches': matches,
        'end_scores': _calc_match_off_end_scores(matches)
    }


def _calc_match_off_end_scores(matches):
    # TODO merge with _calc_match_end_scores
    scores = defaultdict(int)

    for match_results in matches:
        for game_result in match_results:
            winners = game_result['end_scores']['winner']

            for winner in winners:
                desc_winner = _get_description_winner(winner)
                scores[desc_winner] += 1

    import operator
    return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    #  'scores': scores,
    #  'ranking': sorted(scores, key= lambda score: scores[score])


def _get_description_winner(winner: dict) -> str:
    if winner == 'exaequo':
        return 'exaequo'
    return winner['class'] + ":" + str(winner['configuration'])


def _run_match(bots, nr_of_games) -> dict:
    """1 match (with bot-config-pair) = m games"""

    start, game_results = datetime.now().timestamp(), _run_games(nr_of_games, bots)
    match_duration = datetime.now().timestamp() - start

    match_json = _match_result(game_results, bots, match_duration)
    _print_end_score_to_console(match_json, match_duration)
    return match_json


def _match_result(game_results, bots, duration) -> dict:
    return {
        'bots':
            [{
                'id': bot.bot_id,
                'class': bot.__class__.__name__,
                'configuration': bot.get_configuration()
            } for bot in bots],
        'duration': format_time(duration),
        'games': game_results,
        'end_scores': _calc_match_end_scores(game_results, bots)
    }


def _calc_match_end_scores(game_results, bots):
    # TODO merge with _calc_match_off_end_scores

    scores = {
        'X': 0,
        'O': 0,
        'exaequo': 0
    }
    for game_result in game_results:
        scores[game_result['winner']] += 1

    highest_score = max(scores.values())
    scores['winner'] = [_get_full_bot_description_from_id(bots, bot_id) for bot_id in scores
                        if scores[bot_id] == highest_score]

    return scores


# TODO: remove, use short_name of bot instead
def _get_full_bot_description_from_id(bots, bot_id: str):
    if bot_id == 'exaequo':
        return 'exaequo'
    for bot in bots:
        if bot.bot_id == bot_id:
            return {
                'class': bot.__class__.__name__,
                'configuration': bot.get_configuration()
            }


# TODO: keep this?
def _print_end_score_to_console(victories: dict, timestamp):
    print("{} games played.\n".format(len(victories['games'])))
    print("End score:\n")
    victories_json = json.dumps(victories, indent=4)
    print(victories_json)
    print("\nDuration: " + format_time(timestamp))


def _run_games(nr_of_games, bots) -> list:
    game_results = []
    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write('{:3}'.format('#{}'.format(i + 1)))
        game_results.append(_run_one_game(bots))
    return game_results


def _run_one_game(bots) -> dict:
    grid = Grid()
    players = [bot for bot in bots]  # clone
    random.shuffle(players)

    i, progress = 0, ProgressBar()
    while not grid.game_over() and not grid.is_full():
        progress.next()
        i = (i + 1) % 2
        start, column, end = time(), players[i].choose_move(grid), time()
        with open("../../docs/times/times.txt", 'a') as writer:
            writer.write("{} : {}\n".format(players[i], end - start))
        grid.add_pawn(column, players[i].bot_id)
    progress.end()

    return _game_result(grid)


def _game_result(grid) -> dict:
    return {
        'winner': grid.game_over(),
        'end_configuration': grid.get_state_string_representation()
    }
