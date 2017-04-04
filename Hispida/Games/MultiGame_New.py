import sys, os

sys.path.insert(0, os.path.abspath("."))

import random, json
from time import localtime
from datetime import datetime
from Games.ProgressBar import ProgressBar

from Grid.Grid import ColumnGrid
from Robots.MinmaxRobot_ZeroHeuristic import MinmaxRobot_ZeroHeuristic
from Robots.MinmaxRobot import MinmaxRobot

STANDARD_NR_OF_GAMES = 3
TEST_ROUND_RESULTS_FOLDER = "test_round_results/"


def get_robot_from_id(robots, id: str):
    if id == 'exaequo':
        return 'exaequo'
    for robot in robots:
        if robot.robot_id == id:
            return robot


def get_class_name_player(player):
    if player == 'exaequo':
        return player
    else:
        return str(player.__class__.__name__)


def pretty_print_time(time):
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = (time % 60) // 1
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s\n"


def get_time():
    time_string = str(localtime()[1]) + "M" + \
                  str(localtime()[2]) + "D_" + \
                  str(localtime()[3]) + "h" + \
                  str(localtime()[4]) + "m"
    return time_string


def print_end_score_to_console(victoriesDict, time):
    print(str(len(victoriesDict['games'])) + " games played.\n")
    print("End score:\n")
    victories_json = json.dumps(victoriesDict, indent=4)
    print(victories_json)
    print("\nDuration: " + pretty_print_time(time))


def print_end_score_to_file(victoriesDict, time, print_folder):
    victors = list(victoriesDict.keys())
    victor_names = [robot.__class__.__name__ for robot in victors if type(robot) != str]
    file_name = print_folder + victor_names[0] + "_vs_" + victor_names[1] + "@" + get_time() + ".txt"

    writer = open(file_name, 'w')
    writer.write(str(STANDARD_NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for index in range(len(victors)):
        writer.write(get_class_name_player(victors[index]) + " : " + str(victoriesDict.get(victors[index])) + "\n")

    writer.write("\nDuration: " + pretty_print_time(time) + "\n")

    writer.write("Additional details robots:\n")
    for index in range(len(victors)):
        if victors[index] != 'exaequo':
            writer.write(
                get_class_name_player(victors[index]) + " : " + str(victors[index].get_configuration() + "\n"))
    writer.close()


def game_result(robots, grid) -> dict:
    game_result = {}
    winner = get_robot_from_id(robots, grid.game_over())
    if type(winner) == str:
        game_result['winner'] = winner
    else:
        game_result['winner'] = winner.robot_id
    game_result['end_configuration'] = grid.show_state()
    return game_result


def run_one_game(robots) -> dict:
    grid = ColumnGrid()
    players = [robot for robot in robots]  # clone
    random.shuffle(players)

    progress = ProgressBar()
    progress.next()
    i = 0
    while grid.game_over() == -1 and grid.get_free_columns() != []:
        i = (i + 1) % 2
        column = players[i].choose_move(grid)
        grid.add_pawn(column, players[i].robot_id)
        progress.next()
    progress.end()

    return game_result(robots, grid)


def run_games(nr_of_games, robots) -> list:
    game_results = []
    # TODO rename victoriesDict?
    victoriesDict = {'exaequo': 0}
    for robot in robots:
        victoriesDict[robot] = 0

    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write("#" + str(i + 1) + " " * (4 - len(str(i + 1))))

        game_results.append(run_one_game(robots))

        victor_id = game_results[-1]['winner']
        robot = get_robot_from_id(robots, victor_id)
        victoriesDict[robot] = victoriesDict[robot] + 1
    return game_results


def find_end_scores_winners_2(scores):
    highest_score = max(scores.values())

    return [score for score in scores if scores[score] == highest_score]


@DeprecationWarning
def find_end_scores_winners(scores, robots):
    highest_score = scores[max(scores, key=lambda score: scores[score])]

    if len([score for score in scores if scores[score] == highest_score]) == 1:
        winner_robot = get_robot_from_id(robots, max(scores, key=lambda score: scores[score]))
        return {
            'class': winner_robot.__class__.__name__,
            'configuration': winner_robot.get_configuration()
        }
    else:
        return {
            'exaequo': [get_robot_from_id(robots, score) for score in scores if scores[score] == highest_score]
        }


def calculate_end_scores(game_results, robots):
    scores = {
        'X': 0,
        'O': 0,
        'exaequo': 0
    }
    for game_result in game_results:
        scores[game_result['winner']] += 1

    scores['winner'] = find_end_scores_winners(scores, robots)

    return scores


def test_result(game_results, robots, duration) -> dict:
    test_result = {}
    test_result['robots'] = []
    for i in range(len(robots)):
        test_result['robots'].append({
            'id': robots[i].robot_id,
            'class': robots[i].__class__.__name__,
            'configuration': robots[i].get_configuration()
        })
    test_result['duration'] = pretty_print_time(duration)
    test_result['games'] = game_results
    test_result['end_scores'] = calculate_end_scores(game_results, robots)
    return test_result


def run_test(robots, nr_of_games) -> dict:
    # 1 test (with robot-config-pair) = m games

    from datetime import datetime
    start = datetime.now().timestamp()
    game_results = run_games(nr_of_games, robots)
    end = datetime.now().timestamp()

    test_duration = end - start

    test_json = test_result(game_results, robots, test_duration)

    print_end_score_to_console(test_json, test_duration)

    # test_result = test_result(game_results, robots, end_scores, test_duration)

    # for victor in game_results:
    #    test_result['end_scores'][victor] = game_results['victor']

    return test_json


def calc_test_round_end_scores(test_results):
    # TODO re-use find_end_scores_winners?
    scores = {}

    for test_result in test_results:
        winner = test_result['winner']
        if winner in scores:
            scores[winner] += 1
        else:
            scores[winner] = 1

    return {
        'scores': scores,
        'ranking': sorted(scores)
    }


# 1 test -> n games
def test_round_result(test_results, start_time) -> dict:
    test_round_result = {}
    test_round_result['time'] = start_time
    test_round_result['tests'] = test_results
    test_round_result['end_scores'] = calc_test_round_end_scores(test_results)
    return test_round_result


def print_to_file(file_name, json):
    with open(file_name, 'w') as writer:
        writer.write(str(json))


def run_test_test_round():
    independent_variable = MinmaxRobot_ZeroHeuristic('O')
    dependent_variable = MinmaxRobot('X')

    from datetime import datetime
    start_time = datetime.now().timestamp()
    test_results = []

    for heuristic_robot in range(-2, -1):
        for heuristic_opponent in range(-2, 0):
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)
            test_result = run_test((independent_variable, dependent_variable), nr_of_games=2)
            test_results.append(test_result)

    sys.stdout.write("\n\nMultiple tests done.")
    file_name = "test_round_results/test_test_round.json"
    import json
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(file_name, results_json)


# STRUCTURE
# 1 test round = n tests
# 1 test = 2 robots with configs = m games
def run_test_round_A():
    """1 test round = n tests (each with robot-config-pair) = n*m games"""

    independent_variable = MinmaxRobot_ZeroHeuristic('O')
    dependent_variable = MinmaxRobot('X')

    start_time = datetime.now().isoformat()

    test_results = []
    for heuristic_robot in range(-2, 3):
        for heuristic_opponent in range(-2, 3):
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)
            test_result = run_test((independent_variable, dependent_variable), nr_of_games=30)
            test_results.append(test_result)

    sys.stdout.write("\n\nMultiple tests done.")
    file_name = "test_round_A.json"
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)


def run_test_round_B():
    independent_variable = MinmaxRobot_ZeroHeuristic('O')
    dependent_variable = MinmaxRobot('X')

    start_time = datetime.now().isoformat()

    test_results = []
    for heuristic_robot in range(0, 4):  # 0,4
        for heuristic_opponent in range(-3, 1):  # -3,1
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)
            test_result = run_test((independent_variable, dependent_variable), nr_of_games=30)
            test_results.append(test_result)

    sys.stdout.write("\n\nMultiple tests done.")
    file_name = "test_round_B.json"
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)


def run_test_round_C():
    PRINT_FOLDER_C = "Results_C/"
    var_1 = MinmaxRobot('O')
    var_2 = MinmaxRobot('X')

    winner_heuristic_scores = [(1, -3), (1, 0), (1, -2), (2, -1), (2, 0), (3, -1), (3, 0)]

    for i in range(len(winner_heuristic_scores)):
        for j in range(i + 1, len(winner_heuristic_scores)):
            var_1.set_heuristic_parameters(heuristic_robot=winner_heuristic_scores[i][0],
                                           heuristic_opponent=winner_heuristic_scores[i][1])
            var_2.set_heuristic_parameters(heuristic_robot=winner_heuristic_scores[j][0],
                                           heuristic_opponent=winner_heuristic_scores[j][1])
            run_test([var_1, var_2], nr_of_games=30, print_folder=PRINT_FOLDER_C)

    sys.stdout.write("\n\nMultiple tests done.")


run_test_round_A()
