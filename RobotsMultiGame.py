from Grid import ColumnGrid
from Robots.MinusFirstOrderRobot import MinusFirstOrderRobot
from Robots.FirstOrderRobot import FirstOrderRobot
from Robots.ZeroOrderRobot import ZeroOrderRobot

robot1 = FirstOrderRobot()
robot2 = MinusFirstOrderRobot()

def start():
    humanPlayerId = 'X'
    robotPlayerId = 'O'
    grid = ColumnGrid()

    print("\nWelcome to a new game of Connect 4\n")

    robot = choose_opponent()

    print("To exit the game press Q + ENTER\n")
    print("Please do the first move")

    # try:
    while grid.game_over() == -1:
        grid.print_grid()
        column = accept_human_move(grid)
        grid.add_pawn(column, humanPlayerId)

        if grid.game_over() != -1:
            break

        column = robot.choose_move(grid)
        grid.add_pawn(column, robotPlayerId)

    grid.print_grid()
    print("\nPlayer " + str(grid.game_over()) + " won, congrats!\n")


# except Exception as exc:
# print(exc.__str__())
start()
