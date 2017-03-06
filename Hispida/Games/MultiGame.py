import random

from Grid.Grid import ColumnGrid
from Robots.ManyOrderRobot import ManyOrderRobot
from Robots.FirstOrderRobot import FirstOrderRobot

ROBOT_1 = FirstOrderRobot('X')
ROBOT_2 = ManyOrderRobot('O')

NR_OF_GAMES = 3


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
    try:
        while grid.game_over() == -1 and grid.get_free_columns() != []:
            i = (i + 1) % 2
            column = players[i].choose_move(grid)
            grid.add_pawn(column, players[i].robotId)

            if grid.game_over() != -1:
                robot = getRobotFromId(victoriesDict, grid.game_over())
                victoriesDict[robot] = victoriesDict[robot] + 1
                break
    except Exception as ex:
        grid.print_grid()
        raise ex


def get_name_player(player):
    if player == 'exaequo':
        return player
    else:
        return str(player.__class__.__name__)


def print_end_score_to_console(NR_OF_GAMES, robots, victoriesDict, time):
    print(str(NR_OF_GAMES) + " games played.\n")
    print("End score:\n")
    for robot in robots:
        print(get_name_player(robot) + " : " + str(victoriesDict.get(robot)) + "\n")

    print("Time: " + str(time))


def print_end_score_to_file(NR_OF_GAMES, robots, victoriesDict, time):
    # TODO give files specific names like "ZeroOrderRobot_vs_FirstOrderRobot.txt"
    writer = open('endScore.txt', 'w')

    writer.write(str(NR_OF_GAMES) + " games played.\n")
    writer.write("End score:\n")
    for robot in robots:
        writer.write(get_name_player(robot) + " : " + str(victoriesDict.get(robot)) + "\n")

    writer.write("Time: " + str(time))
    writer.close()


def start(NR_OF_GAMES):
    from datetime import datetime

    start = datetime.now().timestamp()

    victoriesDict = {ROBOT_1: 0, ROBOT_2: 0, 'exaequo': 0}

    while NR_OF_GAMES > 0:
        print(str(NR_OF_GAMES))
        run_game(victoriesDict)
        NR_OF_GAMES -= 1

    end = datetime.now().timestamp()

    robots = list(victoriesDict.keys())
    print_end_score_to_console(NR_OF_GAMES, robots, victoriesDict, end - start)


start(NR_OF_GAMES)
