from Robots.FirstOrderRobot import FirstOrderRobot

from math import inf


class MinmaxRobot(FirstOrderRobot):
    """Applies a minmax algorithm. Only 2n+1 iterations considered. should only work for values 2n+1."""

    WIN_SCORE = 20
    LOSE_SCORE = -1
    EXAEQUO_SCORE = 0
    DEPTH = 5
    HEURISTIC_ROBOT = 2
    HEURISTIC_OPPONENT = 1

    def set_parameters(self, win_score=WIN_SCORE, exaequo_score=EXAEQUO_SCORE, depth=DEPTH):
        self.WIN_SCORE = win_score
        self.EXAEQUO_SCORE = exaequo_score
        self.DEPTH = depth

    def set_heuristic_parameters(self, heuristic_robot=HEURISTIC_ROBOT, heuristic_opponent=HEURISTIC_OPPONENT):
        self.HEURISTIC_ROBOT = heuristic_robot
        self.HEURISTIC_OPPONENT = heuristic_opponent

    def get_configuration(self) -> dict:
        # TODO: automatically iterate over fields of instance
        return {
            "WIN_SCORE": self.WIN_SCORE,
            "LOSE_SCORE": self.LOSE_SCORE,
            "EXAEQUO_SCORE": self.EXAEQUO_SCORE,
            "DEPTH": self.DEPTH,
            "HEURISTIC_ROBOT": self.HEURISTIC_ROBOT,
            "HEURISTIC_OPPONENT": self.HEURISTIC_OPPONENT,
        }

    def apply_leaf_heuristic(self, grid) -> int:
        xCo = grid.get_last_move()[0]
        yCo = grid.get_filled_top_index(xCo)
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(xCo, yCo):
            if tile == self.robot_id:
                heuristic_score += self.HEURISTIC_ROBOT
            elif tile == self.get_id_opponent():
                heuristic_score += self.HEURISTIC_OPPONENT
        return heuristic_score

    def alpha_beta(self, grid, depth: int, alpha: int, beta: int, max_not_min: bool):
        if depth == 0:
            return self.apply_leaf_heuristic(grid)
        if grid.game_over() == 'exaequo':
            return self.EXAEQUO_SCORE
        if grid.game_over() == self.robot_id:
            return self.WIN_SCORE
        if grid.game_over() == self.get_id_opponent():
            return self.LOSE_SCORE

        if max_not_min:
            v = -inf
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move(x, self.robot_id)
                v = max(v, self.alpha_beta(new_grid, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        else:
            v = +inf
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move(x, self.get_id_opponent())
                v = min(v, self.alpha_beta(new_grid, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return v

    def choose_move_with_minmax(self, grid) -> int:
        # Like max iteration except must remember move.
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robot_id)

            moves_scores.append({'move': x, 'score': self.alpha_beta(new_grid, self.DEPTH - 1, -inf, +inf, False)})

        return max(moves_scores, key=lambda move: move['score'])['move']

    def choose_move(self, grid):
        # First two checks speed up and make robot better.
        if self.check_if_immediate_win_possible(grid):
            return self.check_if_immediate_win_possible(grid)['column']
        elif grid.get_nr_moves_left() == 1:
            return grid.get_free_columns()[0]
        else:
            return self.choose_move_with_minmax(grid)
