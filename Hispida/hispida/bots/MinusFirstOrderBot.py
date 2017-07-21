import random

from Bot import Bot


class MinusFirstOrderBot(Bot):
    def choose_move(self, grid):
        return random.choice(grid.get_free_columns())
