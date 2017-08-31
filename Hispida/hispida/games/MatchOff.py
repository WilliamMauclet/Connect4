import random, json, sys, ast
from time import time
from datetime import datetime
from collections import defaultdict

from Bot import Bot
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
    """The given bots participate in a round-robin tournament to determine the best."""

    planned_matches = _get_planned_matches(bots, file_path)
    total_number_matches = len(bots) * (len(bots) - 1) // 2

    for planned_match in planned_matches:
        sys.stdout.write("TEST {}/{}\n".format(planned_match['number'], total_number_matches))
        planned_match['i'].bot_id, planned_match['j'].bot_id = 'X', 'O'
        match_result = _run_match((planned_match['i'], planned_match['j']), nr_of_games=nr_of_games)

        if match_result:
            with open(file_path, 'a') as writer:
                writer.write("{}\n".format(match_result))  # TODO

        results = _match_off_result(total_number_matches, file_path)
        pass


def _get_planned_matches(bots, file_path):
    match_number, planned_matches = 0, []
    left_off_line = _calculate_where_left_off(file_path)
    for i, bot_i in enumerate(bots):
        for bot_j in bots[i + 1:]:
            match_number += 1
            if match_number < left_off_line:
                continue

            planned_matches.append({'number': match_number, 'i': bot_i, 'j': bot_j})

    return planned_matches


def _calculate_where_left_off(file_path) -> int:
    try:
        with open(file_path, 'r') as reader:
            return reader.read().count("\n")
    except FileNotFoundError:
        return 0


def _match_off_result(total_number_of_matches, file_path) -> dict:
    matches = []
    with open(file_path, 'r') as reader:
        for _ in range(total_number_of_matches):
            matches.append(ast.literal_eval(reader.readline()))

    scores = defaultdict(int)
    for match_result in matches:
        for bot_descr in match_result['scores']:
            scores[bot_descr] += match_result['scores'][bot_descr]

    return {
        'winners': [bot_descr for bot_descr in scores if scores[bot_descr] == max(scores.values())],
        'scores': scores,
        'matches': matches
    }


def _run_match(bots, nr_of_games) -> dict:
    """1 match (with bot-config-pair) = m games"""

    start, game_results = datetime.now().timestamp(), _run_games(nr_of_games, bots)
    match_duration = datetime.now().timestamp() - start

    match_json = _match_result(game_results, bots, match_duration)
    _print_match_end_score(match_json, match_duration)
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
        'end_scores': _calc_match_end_scores(game_results)
    }


def _calc_match_end_scores(game_results):
    scores = defaultdict(int)
    for game_result in game_results:
        scores[game_result['winner']] += 1

    return {
        'winners': [bot_descr for bot_descr in scores if scores[bot_descr] == max(scores.values())],
        'scores': scores
    }


def _print_match_end_score(victories: dict, timestamp):
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
    players = [bot for bot in bots]
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

    return _game_result(grid, bots)


def _game_result(grid, bots) -> dict:
    return {
        'winner': _get_bot_descriptor_from_id(bots, grid.game_over()),
        'end_configuration': grid.get_state_string_representation()
    }


def _get_bot_descriptor_from_id(bots: [Bot], bot_id: str) -> str:
    if bot_id == 'exaequo':
        return 'exaequo'
    for bot in bots:
        if bot.bot_id == bot_id:
            return bot.get_descriptor()
