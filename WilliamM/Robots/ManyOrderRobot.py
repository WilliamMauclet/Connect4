import random

from WilliamM.Robots.FirstOrderRobot import FirstOrderRobot


class ManyOrderRobot(FirstOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create a future win possibility for the opponent.
    Except for that, it just plays randomly."""

    #TODO
    def evaluate_tail(self, grid, playerId):
        result = grid.game_over()
        if result == playerId:
            return 1
        elif result == 'exaequo':
            return 0
        else:
            return -1

    def trivial_case_recursion(self, grid, playerId):
        """Tail of the recursion. Should return a dictionary with keys from 0 to 6 and a score for each.
        If victory possible for player: +1, if not: 0. In negative if opponent."""
        moves_scores = []
        for move in grid.get_free_columns():
            new_grid = grid.clone()
            new_grid.addPawn(move, self.robotId)

            moves_scores.append(self.evaluate_tail(new_grid, playerId))

        return max(moves_scores) # TODO What if only 0s???

    def recursive_case_recursion(self, grid, playerId, lookAheadsLeft):
        """Trunk of the recursion. Should combine the scores from further recursion executions."""
        moves_scores = []
        opponent_id = self.get_id_opponent()
        for move in grid.get_free_columns():
            new_grid = grid.clone()
            new_grid.addPawn(move, playerId)
            if new_grid.game_over() == playerId:
                return 1
            elif new_grid.game_over() == opponent_id:
                return -1
            else:
                if lookAheadsLeft == 1:
                    moves_scores.append(-1 * self.trivial_case_recursion(new_grid, opponent_id))
                else:
                    moves_scores.append(-1 * self.recursive_case_recursion(new_grid, opponent_id, lookAheadsLeft-1))


        raise NotImplementedError("Details not found yet.")

    #TODO

    def choose_move_that_does_not_help_opponent(self, grid):
        """TODO Should give score to every column > choose (randomly from) column(s) with highest score"""
        freeColumns = grid.get_free_columns()
        dangerousColumns = []

        for x in freeColumns:
            column = self.evaluate_column_does_not_help_opponent(grid, x)
            if column is not None:
                dangerousColumns.append(column)

        if len(freeColumns) == len(dangerousColumns):
            return random.choice(freeColumns)
        else:
            return random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_columns(grid, freeColumns) != -1:
            return self.check_columns(grid, freeColumns)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
