import sys,os
sys.path.insert(0, os.path.abspath("."))

import random
from time import localtime
from Games.ProgressBar import ProgressBar

from Grid.Grid import ColumnGrid
from Robots.FirstOrderRobot import FirstOrderRobot as second_robot
from Robots.ManyOrderRobot_c import ManyOrderRobot_C as first_robot

ROBOT_2 = second_robot('O')
ROBOT_1 = first_robot('X')

NR_OF_GAMES = 3
TO_FILE = True


def getRobotFromId(dict, id):
    if id == 'exaequo':
        return 'exaequo'
    robots = list(dict.keys())
    for robot in robots:
        if robot.robotId == id:
            return robot


def run_game(victoriesDict):
    grid = ColumnGrid()
    players = [ROBOT_1, ROBOT_2]
    random.shuffle(players)
    i = 0
    progress = ProgressBar()
    progress.next()
    try:
        while grid.game_over() == -1 and grid.get_free_columns() != []:
            i = (i + 1) % 2
            column = players[i].choose_move(grid)
            grid.add_pawn(column, players[i].robotId)

            if grid.game_over() != -1:
                robot = getRobotFromId(victoriesDict, grid.game_over())
                victoriesDict[robot] = victoriesDict[robot] + 1
                break
            if i == i%2:
                progress.next()
    except Exception as ex:
        print_end_score_to_console(players, victoriesDict, 0)
        grid.print_grid()
        raise ex
    progress.end()



def get_name_player(player):
    if player == 'exaequo':
        return player
    else:
        return str(player.__class__.__name__)


def print_end_score_to_console(robots, victoriesDict, time):
    print(str(NR_OF_GAMES) + " games played.\n")
    print("End score:\n")
    for robot in robots:
        print(get_name_player(robot) + " : " + str(victoriesDict.get(robot)) + "\n")

    print("Time: " + str(time))

def get_time():
    time_string = str(localtime()[1])+"#"+str(localtime()[2])+"_"+str(localtime()[3])+"#"+str(localtime()[4])
    return time_string

def print_end_score_to_file(robots, victoriesDict, time):
    robot_names = [robot.__class__.__name__ for robot in robots]
    file_name = robot_names[0] + "_vs_" + robot_names[1] + "@" + get_time()+ ".txt"

    writer = open(file_name, 'w')

    #TODO add description ManyOrderRobot

    writer.write(str(NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for robot in robots:
        writer.write(get_name_player(robot) + " : " + str(victoriesDict.get(robot)) + "\n")

    writer.write("Time: " + str(time))
    writer.close()


def start():
    from datetime import datetime

    start = datetime.now().timestamp()

    victoriesDict = {ROBOT_1: 0, ROBOT_2: 0, 'exaequo': 0}

    sys.stdout.write("GAME:\n")
    for i in range(NR_OF_GAMES):
        sys.stdout.write("#" + str(i+1) + " ")
        #print("#" + str(i+1))
        run_game(victoriesDict)

    end = datetime.now().timestamp()

    robots = list(victoriesDict.keys())
    if TO_FILE:
        print_end_score_to_file(robots, victoriesDict, end - start)

    print_end_score_to_console(robots, victoriesDict, end - start)


start()
