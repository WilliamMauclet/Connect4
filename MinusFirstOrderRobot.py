import random


class MinusFirstOrderRobot():
    def choose_move(self, grid):
        return random.choice(grid.get_free_columns())
