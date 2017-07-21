import random

from ZeroOrderBot import ZeroOrderBot


class FirstOrderBot(ZeroOrderBot):
    """This bot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
    Except for that, it just plays randomly."""

    def does_move_help_opponent(self, grid, x) -> bool:
        new_grid = grid.clone_with_move(x, self.bot_id)
        return \
            self.check_if_immediate_win_possible(new_grid) \
            and self.is_id_opponent(self.check_if_immediate_win_possible(new_grid)['player'])

    def choose_move_that_does_not_help_opponent(self, grid) -> int:
        free_columns, dangerous_columns = grid.get_free_columns(), []
        for x in free_columns:
            if self.does_move_help_opponent(grid, x):
                dangerous_columns.append(x)
        if len(free_columns) == len(dangerous_columns):
            self.log("GAME IS LOST WHATEVER MOVE I MAKE")
            return random.choice(free_columns)
        return random.choice([i for i in free_columns if i not in dangerous_columns])

    def choose_move(self, grid):
        if self.check_if_immediate_win_possible(grid):
            return self.check_if_immediate_win_possible(grid)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
