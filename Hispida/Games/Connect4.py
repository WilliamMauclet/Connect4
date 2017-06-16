import sys, os

sys.path.insert(0, os.path.abspath("."))

from Grid.Grid import Grid


def accept_human_move(grid):
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    acceptedInputs = ['q', 'Q'] + [str(x + 1) for x in grid.get_free_columns()]
    while inp not in acceptedInputs:
        inp = input("Please give one of the following values: " + str(acceptedInputs) + "\n")

    if inp == 'q' or inp == 'Q':
        raise Exception("Game finished by player")
    else:
        return int(inp) - 1


def accept_human_move_prev(grid):
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    if inp is 'q':
        raise Exception("Game aborted")
    column = int(inp) - 1
    while not grid.is_column_free(column):
        inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
        if inp is 'q':
            raise Exception("Game aborted")
        column = int(inp) - 1
    return column


def choose_opponent() -> None:
    print("Choose an opponent against whom to play:\n")

    inp = None
    acceptedInputs = ['', '-1', '0', '1', '2', '3']
    while inp not in acceptedInputs:
        inp = input(
            "-1 for MinusOneOrderRobot, 0 for ZeroOrderRobot, 1 for FirstOrderRobot, 2 for MinmaxRobot, 3 for MinmaxRobot(alpha-beta) (last=default): ")
    if inp is "":
        inp = acceptedInputs[-1]
    global ROBOT
    if inp == '-1':
        print("\nThis game is against an opponent playing randomly.\n")
        from Robots.MinusFirstOrderRobot import MinusFirstOrderRobot
        ROBOT = MinusFirstOrderRobot(ROBOT_PLAYER_ID)
    elif inp == '0':
        print("\nThis game is against an opponent playing randomly but avoiding simple traps.\n")
        from Robots.ZeroOrderRobot import ZeroOrderRobot
        ROBOT = ZeroOrderRobot(ROBOT_PLAYER_ID)
    elif inp == '1':
        print("\nThis game is against an opponent playing randomly but avoiding (/to make) simple traps.\n")
        from Robots.FirstOrderRobot import FirstOrderRobot
        ROBOT = FirstOrderRobot(ROBOT_PLAYER_ID)
    elif inp == '2':
        print("\nThis game is against an opponent using a minmax algorithm without alpha-beta pruning.\n")
        from Robots.previous.MinmaxRobot_WithoutAlphaBeta import MinmaxRobot_WithoutAlphaBeta
        ROBOT = MinmaxRobot_WithoutAlphaBeta(ROBOT_PLAYER_ID)
        ROBOT.set_heuristic_parameters(heuristic_robot=2, heuristic_opponent=1)
    elif inp == '3':
        print("\nThis game is against an opponent using a minmax algorithm with alpha-beta pruning")
        from Robots.MinmaxRobot import MinmaxRobot
        ROBOT = MinmaxRobot(ROBOT_PLAYER_ID)
        ROBOT.set_heuristic_parameters(heuristic_robot=2, heuristic_opponent=1)
        ROBOT.DEPTH = 7
    else:
        raise Exception("Did not recognise robot id: '" + inp + "'")


def start():
    grid = Grid()
    print("\nWelcome to a new game of Connect 4\n")
    choose_opponent()
    print("To exit the game press Q + ENTER\n")
    print("Please make the first move")

    id_index = 1
    grid.print_grid()
    while grid.game_over() == -1:
        id_index = (id_index + 1)%2
        id = [HUMAN_PLAYER_ID, ROBOT_PLAYER_ID][id_index]
        accept_move(grid, id)
        grid.print_grid()
        if grid.game_over() != -1:
            break

    print(get_player_tag_from_id(str(grid.game_over())) + " won, congrats!\n")


def accept_move(grid, id):
    if id == HUMAN_PLAYER_ID:
        column = accept_human_move(grid)
    else:
        column = ROBOT.choose_move(grid)

    print(get_player_tag_from_id(id) + " played column: " + str(column + 1))
    grid.add_pawn(column, id)


def get_player_tag_from_id(id):
    if id == HUMAN_PLAYER_ID:
        return "You"
    else:
        return "Robot"


# change here if you want to get more messages.
import logging

logging.getLogger().setLevel(logging.CRITICAL)
# except Exception as exc:
# print(exc.__str__())

HUMAN_PLAYER_ID = 'X'
ROBOT_PLAYER_ID = 'O'


start()
