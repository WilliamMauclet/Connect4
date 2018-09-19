import random

from hispida.bots.Bot import Bot


class MinusFirstOrderBot(Bot):
    def choose_move(self, grid):
        return random.choice(list(grid.get_free_columns()))
