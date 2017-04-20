from Robots.FirstOrderRobot import FirstOrderRobot


class MinmaxRobot_WithoutAlphaBeta(FirstOrderRobot):
    """Applies a minmax algorithm. Only 2n+1 iterations considered. should only work for values 2n+1."""

    WIN_SCORE = 20
    LOSE_SCORE = -1
    EXAEQUO_SCORE = 0
    DEPTH = 5
    HEURISTIC_ROBOT = 2
    HEURISTIC_OPPONENT = 1

    def set_parameters(self, win_score=WIN_SCORE, exaequo_score=EXAEQUO_SCORE, DEPTH=DEPTH):
        self.WIN_SCORE = win_score
        self.EXAEQUO_SCORE = exaequo_score
        self.DEPTH = DEPTH

    def set_heuristic_parameters(self, heuristic_robot=HEURISTIC_ROBOT, heuristic_opponent=HEURISTIC_OPPONENT):
        self.HEURISTIC_ROBOT = heuristic_robot
        self.HEURISTIC_OPPONENT = heuristic_opponent

    def get_configuration(self) -> dict:
        return {
            "WIN_SCORE": self.WIN_SCORE,
            "LOSE_SCORE": self.LOSE_SCORE,
            "EXAEQUO_SCORE": self.EXAEQUO_SCORE,
            "DEPTH": self.DEPTH,
            "HEURISTIC_ROBOT": self.HEURISTIC_ROBOT,
            "HEURISTIC_OPPONENT": self.HEURISTIC_OPPONENT,
        }

    def apply_leaf_heuristic(self, grid, xCo) -> int:
        """Heuristic score based on how good the last move is."""
        yCo = grid.get_filled_top_index(xCo)
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(xCo, yCo):
            if tile == self.robot_id:
                heuristic_score += self.HEURISTIC_ROBOT
            elif tile == self.get_id_opponent():
                heuristic_score += self.HEURISTIC_OPPONENT
        return heuristic_score

    def iteration(self, grid, DEPTH_left: int, maxNotMin: bool) -> int:
        moves_scores = []
        for x in grid.get_free_columns():
            robot_id = self.robot_id if maxNotMin else self.get_id_opponent()
            new_grid = grid.clone_with_move(x, robot_id) # ERROR!!! => should sometimes be id of opponent!
            if new_grid.game_over() == self.robot_id:
                return self.WIN_SCORE
            elif new_grid.game_over() == self.get_id_opponent():
                return self.LOSE_SCORE
            elif new_grid.game_over() == 'exaequo':
                moves_scores.append(self.EXAEQUO_SCORE)
            elif DEPTH_left == 1:
                moves_scores.append(self.apply_leaf_heuristic(new_grid, x))
            else:
                moves_scores.append(self.iteration(new_grid, DEPTH_left - 1, not maxNotMin))

        if maxNotMin:
            return max(moves_scores)
        else:
            return min(moves_scores)

    def choose_move_with_minmax(self, grid) -> int:
        """Like max iteration except must remember move."""
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robot_id)
            moves_scores.append({'move': x, 'score': self.iteration(new_grid, self.DEPTH - 1, maxNotMin=False)})

        return max(moves_scores, key=lambda move: move['score'])['move']

    def choose_move(self, grid):
        if self.check_if_immediate_win_possible(grid):
            #TODO this line won't be necessary with alpha-beta pruning
            return self.check_if_immediate_win_possible(grid)['column']
        elif grid.get_nr_moves_left() == 1:
            return grid.get_free_columns()[0]
        else:
            return self.choose_move_with_minmax(grid)
