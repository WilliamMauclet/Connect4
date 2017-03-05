import random

from Hispida.Grid import ColumnGrid
from Hispida.Robots.ManyOrderRobot import ManyOrderRobot
from Hispida.Robots.FirstOrderRobot import FirstOrderRobot

ROBOT_1 = FirstOrderRobot('X')
ROBOT_2 = ManyOrderRobot('O')

NR_OF_GAMES = 200


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


def start(NR_OF_GAMES):
    victoriesDict = {ROBOT_1: 0, ROBOT_2: 0, 'exaequo': 0}

    while NR_OF_GAMES > 0:
        print(str(NR_OF_GAMES))
        run_game(victoriesDict)
        NR_OF_GAMES -= 1

    robots = list(victoriesDict.keys())
    print(str(NR_OF_GAMES) + " games played.\n")
    print("End score:\n")
    for r in range(0, len(robots)):
        print(str(robots[r]) + " : " + str(victoriesDict.get(robots[r])))


# except Exception as exc:
# print(exc.__str__())
start(NR_OF_GAMES)
