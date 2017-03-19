import sys, os

sys.path.insert(0, os.path.abspath("."))

import random
from time import localtime
from Games.ProgressBar import ProgressBar

from Grid.Grid import ColumnGrid
from Robots.MinmaxRobot_ZeroHeuristic import MinmaxRobot_ZeroHeuristic
from Robots.MinmaxRobot import MinmaxRobot

STANDARD_NR_OF_GAMES = 1
TO_FILE = True


# TODO JSONification


def getRobotFromId(robots, id):
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


def format_time(time):
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = (time % 60) // 1
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s\n"


def get_time():
    time_string = str(localtime()[1]) + "M" + str(localtime()[2]) + "D_" + str(localtime()[3]) + "h" + str(
        localtime()[4]) + "m"
    return time_string


def print_end_score_to_console(victoriesDict, time):
    victors = list(victoriesDict.keys())
    print(str(STANDARD_NR_OF_GAMES) + " games played.\n")
    print("End score:\n")
    for victor in victors:
        print(get_class_name_player(victor) + " : " + str(victoriesDict.get(victor)))

    print("\nDuration: " + format_time(time))


def print_end_score_to_file(victoriesDict, time):
    victors = list(victoriesDict.keys())
    victor_names = [robot.__class__.__name__ for robot in victors if type(robot) != str]
    file_name = "Results/" + victor_names[0] + "_vs_" + victor_names[1] + "@" + get_time() + ".txt"

    writer = open(file_name, 'w')
    writer.write(str(STANDARD_NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for index in range(len(victors)):
        writer.write(get_class_name_player(victors[index]) + " : " + str(victoriesDict.get(victors[index])) + "\n")

    writer.write("\nDuration: " + format_time(time) + "\n")

    writer.write("Additional details robots:\n")
    for index in range(len(victors)):
        if victors[index] != 'exaequo':
            writer.write(
                get_class_name_player(victors[index]) + " : " + victors[index].get_advanced_description() + "\n")
    writer.close()


def run_one_game(robots) -> str:
    grid = ColumnGrid()
    players = [robot for robot in robots]
    random.shuffle(players)
    i = 0
    progress = ProgressBar()
    progress.next()
    while grid.game_over() == -1 and grid.get_free_columns() != []:
        i = (i + 1) % 2
        column = players[i].choose_move(grid)
        grid.add_pawn(column, players[i].robot_id)
        progress.next()

    progress.end()
    return grid.game_over()


def run_games(nr_of_games, robots) -> dict:
    victoriesDict = {'exaequo': 0}
    for robot in robots:
        victoriesDict[robot] = 0

    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write("#" + str(i + 1) + " " * (4 - len(str(i + 1))))

        victor_id = run_one_game(robots)
        robot = getRobotFromId(robots, victor_id)
        victoriesDict[robot] = victoriesDict[robot] + 1

    return victoriesDict


def start(robots, nr_of_games):
    from datetime import datetime
    start = datetime.now().timestamp()

    victories = run_games(nr_of_games, robots)

    end = datetime.now().timestamp()

    if TO_FILE:
        print_end_score_to_file(victories, end - start)
    print_end_score_to_console(victories, end - start)


# start([MinmaxRobot('X'), MinmaxRobot_ZeroHeuristic('O')], STANDARD_NR_OF_GAMES)


def run_multiple_tests_A():
    independent_variable = MinmaxRobot_ZeroHeuristic('O')
    dependent_variable = MinmaxRobot('X')

    for heuristic_robot in range(-2, 3):
        for heuristic_opponent in range(-2, 3):
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)

            start([independent_variable, dependent_variable], nr_of_games=50)

    sys.stdout.write("\n\nMultiple tests done.")

def run_multiple_tests_B():
    independent_variable = MinmaxRobot_ZeroHeuristic('O')
    dependent_variable = MinmaxRobot('X')

    for heuristic_robot in range(0, 4):
        for heuristic_opponent in range(-3, 1):
            dependent_variable.set_heuristic_parameters(heuristic_robot=heuristic_robot,
                                                        heuristic_opponent=heuristic_opponent)

            start([independent_variable, dependent_variable], nr_of_games=25)

    sys.stdout.write("\n\nMultiple tests done.")

run_multiple_tests_B()
