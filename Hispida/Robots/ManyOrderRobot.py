import random

from Hispida.Robots.FirstOrderRobot import FirstOrderRobot


class ManyOrderRobot(FirstOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create a future win possibility for the opponent.
    Except for that, it just plays randomly."""

    #TODO
    def apply_leaf_heuristic(self, grid, playerId):
        return 0

    def evaluate_tail(self, grid, playerId):
        result = grid.game_over()
        if result == playerId:
            return 1
        elif result == 'exaequo':
            return self.apply_leaf_heuristic(grid, playerId)
        else:
            return -1

    def trivial_case_recursion(self, grid, playerId):
        """Tail of the recursion. Should return a dictionary with keys from 0 to 6 and a score for each.
        If victory possible for player: +1, if not: 0. In negative if opponent."""
        moves_scores = []
        for move in grid.get_free_columns():
            new_grid = grid.clone()
            new_grid.add_pawn(move, self.robotId)

            moves_scores.append(self.evaluate_tail(new_grid, playerId))

        return max(moves_scores)

    def recursive_case_recursion(self, grid, playerId, lookAheadsLeft):
        """Trunk of the recursion. Should combine the scores from further recursion executions."""
        moves_scores = []
        opponent_id = self.get_id_opponent()
        if grid.get_free_columns() == 0:
            return 0
        for move in grid.get_free_columns():
            new_grid = grid.clone()
            new_grid.add_pawn(move, playerId)
            if new_grid.game_over() == playerId:
                moves_scores.append(1)
            elif new_grid.game_over() == opponent_id:
                moves_scores.append(-1)
            else:
                if lookAheadsLeft == 1:
                    moves_scores.append(-1 * self.trivial_case_recursion(new_grid, opponent_id))
                else:
                    moves_scores.append(-1 * self.recursive_case_recursion(new_grid, opponent_id, lookAheadsLeft-1))

        return max(moves_scores)

    def find_move_corresponding_to_max(self, moves_scores):
        max_move = {'score':-9999999,'move':-1}
        for x in moves_scores.keys():
            if moves_scores[x] > max_move['score']:
                max_move = {'score': moves_scores[x], 'move':x}
        return max_move['move']

    def start_recursion(self, grid, safeMoves):
        look_ahead_depth = 3

        moves_scores = {}
        for move in safeMoves:
            new_grid = grid.clone()
            new_grid.add_pawn(move, self.robotId)
            if new_grid.game_over() == self.robotId:
                moves_scores[move] = 1
            elif new_grid.game_over() == self.robotId:
                moves_scores[move] = -1
            else:
                if look_ahead_depth == 1:
                    moves_scores[move] = self.trivial_case_recursion(new_grid, self.robotId)
                else:
                    moves_scores[move] = self.recursive_case_recursion(new_grid, self.robotId, look_ahead_depth - 1)

        return self.find_move_corresponding_to_max(moves_scores)
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
            return self.start_recursion(grid, [i for i in freeColumns if i not in dangerousColumns])

            #random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_columns(grid, freeColumns) != -1:
            return self.check_columns(grid, freeColumns)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)