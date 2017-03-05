import random

from Hispida.Robots.Robot import Robot


class MinusFirstOrderRobot(Robot):
    def choose_move(self, grid):
        return random.choice(grid.get_free_columns())
