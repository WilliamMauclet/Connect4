import sys, os

sys.path.insert(0, os.path.abspath("."))

import random, json, time
from time import localtime
from datetime import datetime
from Games.ProgressBar import ProgressBar

from Grid.Grid import Grid
from Robots.MinmaxRobot import MinmaxRobot

STANDARD_NR_OF_GAMES = 3
TEST_ROUND_RESULTS_FOLDER = "test_round_results/"


def get_robot_from_id(robots, id: str):
    if id == 'exaequo':
        return 'exaequo'
    for robot in robots:
        if robot.robot_id == id:
            return robot


def get_full_robot_description_from_id(robots, id: str):
    if id == 'exaequo':
        return 'exaequo'
    for robot in robots:
        if robot.robot_id == id:
            return {
                'class': robot.__class__.__name__,
                'configuration': robot.get_configuration()
            }


def get_class_name_player(player):
    if player == 'exaequo':
        return player
    else:
        return player.__class__.__name__


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
    game_result['end_configuration'] = grid.get_state_string_representation()
    return game_result


def run_one_game(robots) -> dict:
    grid = Grid()
    players = [robot for robot in robots]  # clone
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


def find_end_scores_winners(scores):
    highest_score = max(scores.values())

    return [score for score in scores if scores[score] == highest_score]


def calculate_end_scores(game_results, robots):
    scores = {
        'X': 0,
        'O': 0,
        'exaequo': 0
    }
    for game_result in game_results:
        scores[game_result['winner']] += 1

    scores['winner'] = [get_full_robot_description_from_id(robots, id) for id in find_end_scores_winners(scores)]

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
        winners = test_result['end_scores']['winner']

        for winner in winners:
            desc_winner = get_description_winner(winner)
            if desc_winner in scores:
                scores[desc_winner] += 1
            else:
                scores[desc_winner] = 1

    import operator
    return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    #  'scores': scores,
    #  'ranking': sorted(scores, key= lambda score: scores[score])


def get_description_winner(winner: dict) -> str:
    if winner == 'exaequo':
        return 'exaequo'
    return winner['class'] + ":" + str(winner['configuration'])


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
    independent_variable = OLD_MinmaxRobot('O')
    dependent_variable = MinmaxRobot('X')

    from datetime import datetime
    start_time = datetime.now().timestamp()
    test_results = []

    for heuristic_robot in range(2, 3):
        for heuristic_opponent in range(1, 2):
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)
            independent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                          heuristic_opponent=heuristic_opponent)
            test_result = run_test((independent_variable, dependent_variable), nr_of_games=30)
            test_results.append(test_result)

    sys.stdout.write("\n\nMultiple tests done.")
    file_name = "test_round_results/test_test_round.json"
    import json
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(file_name, results_json)


def calculate_where_left_off(file_name) -> int:
    try:
        with open(file_name, 'r') as reader:
            return reader.read().count("\n")
    except FileNotFoundError:
        return 0


# STRUCTURE
# 1 test round = n tests
# 1 test = 2 robots with configs = m games
def run_test_round(file_name="TODO_RENAME.json"):
    """1 test round = n tests (each with robot-config-pair) = n*m games"""
    # TODO test should resume where left off. => user calculate_Where_left_off NOT YET IMPLEMENTED !!!!!!!!!!!!!
    # e.g. count nr of lines in file and calculate modulo first range

    from Robots.MinmaxRobot import MinmaxRobot
    independent_variable = MinmaxRobot('O')
    dependent_variable = MinmaxRobot('X')

    start_time = datetime.now().isoformat()

    # TODO: refactor how to say how far along (cf. ProgressBar)
    heuristic_robot_range = range(-2, 3)
    heuristic_opponent_range = range(-2, 3)
    total_number_of_tests = len(heuristic_robot_range) * len(heuristic_opponent_range)
    test_number = 0
    test_results = []
    left_off_line = calculate_where_left_off(TEST_ROUND_RESULTS_FOLDER + file_name)
    for heuristic_robot in heuristic_robot_range:
        for heuristic_opponent in heuristic_opponent_range:
            test_number += 1
            if test_number < left_off_line:
                continue

            sys.stdout.write("TEST " + str(test_number) + "/" + str(total_number_of_tests) + "\n")
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)
            test_result = run_test((independent_variable, dependent_variable), nr_of_games=30)
            test_results.append(test_result)
            # temporary save
            with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'a') as writer:
                writer.write(str(test_results).replace("{'robots'", "\n{'robots'"))  # 1 line per test result

    with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'r') as reader:
        st = reader.read().replace("\'", "\"").replace("\n", "")
        test_results = json.loads(st)
    sys.stdout.write("\n\nMultiple tests done.")
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)


def match_off(robots, file_name="match_off.json", nr_of_games=30):
    """The given robots participate in a round-robin tournament to determine a ranking."""
    total_number_of_tests = len(robots) / 2 * (len(robots) - 1)
    test_number = 0
    test_results = []
    left_off_line = calculate_where_left_off(TEST_ROUND_RESULTS_FOLDER + file_name)
    for i in range(len(robots)):
        for j in range(i, len(robots)):
            if i == j:
                continue
            test_number += 1
            if test_number < left_off_line:
                continue
            sys.stdout.write("TEST " + str(test_number) + "/" + str(total_number_of_tests) + "\n")

            robots[i].robot_id = 'X'
            robots[j].robot_id = 'O'

            test_result = run_test((robots[i], robots[j]), nr_of_games=nr_of_games)
            test_results.append(test_result)
        # temporary save
        with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'a') as writer:
            writer.write(str(test_results).replace("{'robots'", "\n{'robots'"))  # 1 line per test result


def match_off_test_round():
    """Define here the robots you want to test against each other. Use then the function match_off."""
    robots = []

    for i in range(-2, -1):
        for j in range(-2, -1):
            robot = MinmaxRobot('Z')
            robot.set_heuristic_parameters(heuristic_robot=i, heuristic_opponent=j)
            robots.append(robot)

    from Robots.MinmaxRobot_ZeroHeuristic import MinmaxRobot_ZeroHeuristic
    robots.append(MinmaxRobot_ZeroHeuristic('Z'))

    # TODO: see if test round still busy!!!
    test_number = get_test_number()
    file_name = "test_" + str(test_number)
    increment_test_number()

    start_time = datetime.now().isoformat()

    match_off(robots, file_name=file_name)

    with open(TEST_ROUND_RESULTS_FOLDER + file_name, 'r') as reader:
        st = reader.read().replace("\'", "\"").replace("\n", "")
        test_results = json.loads(st)
    sys.stdout.write("\n\nRound-robin match-off done.")
    results_json = json.dumps(test_round_result(test_results, start_time), indent=4)
    print_to_file(TEST_ROUND_RESULTS_FOLDER + file_name, results_json)

def get_test_number() -> int:
    with open(TEST_ROUND_RESULTS_FOLDER + "test_nr.txt",'r') as reader:
        return int(reader.read())

def increment_test_number():
    previous = get_test_number()
    with open(TEST_ROUND_RESULTS_FOLDER + "test_nr.txt",'w') as writer:
        writer.write(str(previous + 1))

# run_test_round_A()
# run_test_test_round()
#run_test_round()
match_off_test_round()