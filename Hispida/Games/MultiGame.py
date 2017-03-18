import sys, os

sys.path.insert(0, os.path.abspath("."))

import random
from time import localtime
from Games.ProgressBar import ProgressBar

from Grid.Grid import ColumnGrid
from Robots.HalfWayMinmaxRobot import ManyOrderRobot_b as second_robot
from Robots.MinmaxRobot import MinmaxRobot as first_robot

NR_OF_GAMES = 1
TO_FILE = True


def getRobotFromId(dict, id):
    if id == 'exaequo':
        return 'exaequo'
    robots = list(dict.keys())
    for robot in robots:
        if robot != 'exaequo' and robot.robotId == id:
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


def print_end_score_to_console(robots, victoriesDict, time):
    print(str(NR_OF_GAMES) + " games played.\n")
    print("End score:\n")
    for robot in robots:
        print(get_class_name_player(robot) + " : " + str(victoriesDict.get(robot)))

    print("\nDuration: " + format_time(time))


def print_end_score_to_file(robots, victoriesDict, time):
    robot_names = [robot.__class__.__name__ for robot in robots]
    file_name = robot_names[0] + "_vs_" + robot_names[1] + "@" + get_time() + ".txt"

    writer = open(file_name, 'w')
    writer.write(str(NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for index in range(len(robots)):
        writer.write(get_class_name_player(robots[index]) + " : " + str(victoriesDict.get(robots[index])) + "\n")

    writer.write("\nDuration: " + format_time(time) + "\n")

    writer.write("Additional details robots:\n")
    for index in range(len(robots)):
        if robots[index] != 'exaequo':
            writer.write(get_class_name_player(robots[index]) + " : " + robots[index].get_advanced_description() + "\n")
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
        grid.add_pawn(column, players[i].robotId)
        progress.next()

    progress.end()
    return grid.game_over()


def run_games(nr_of_games, robots) -> dict:
    victories = {'exaequo': 0}
    for robot in robots:
        victories[robot] = 0

    sys.stdout.write("GAME:\n")
    for i in range(nr_of_games):
        sys.stdout.write("#" + str(i + 1) + " ")

        victor_id = run_one_game(robots)
        robot = getRobotFromId(victories, victor_id)
        victories[robot] = victories[robot] + 1

    return victories


def start():
    from datetime import datetime
    start = datetime.now().timestamp()

    robots = [first_robot('X'), second_robot('O')]

    victories = run_games(NR_OF_GAMES, robots)

    end = datetime.now().timestamp()

    robots = list(victories.keys())
    if TO_FILE:
        print_end_score_to_file(robots, victories, end - start)
    print_end_score_to_console(robots, victories, end - start)


# TODO remove exaequo from robots
# TODO JSONification

start()
