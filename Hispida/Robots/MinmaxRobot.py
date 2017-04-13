from Robots.FirstOrderRobot import FirstOrderRobot


class MinmaxRobot(FirstOrderRobot):
    """Applies a minmax algorithm. Only 2n+1 iterations considered. should only work for values 2n+1."""

    WIN_SCORE = 20
    LOSE_SCORE = -1
    EXAEQUO_SCORE = 0
    LOOK_AHEADS = 5
    HEURISTIC_ROBOT = 2
    HEURISTIC_OPPONENT = 1

    def set_parameters(self, win_score=WIN_SCORE, exaequo_score=EXAEQUO_SCORE, look_aheads=LOOK_AHEADS):
        self.WIN_SCORE = win_score
        self.EXAEQUO_SCORE = exaequo_score
        self.LOOK_AHEADS = look_aheads

    def set_heuristic_parameters(self, heuristic_robot=HEURISTIC_ROBOT, heuristic_opponent=HEURISTIC_OPPONENT):
        self.HEURISTIC_ROBOT = heuristic_robot
        self.HEURISTIC_OPPONENT = heuristic_opponent

    def get_configuration(self) -> dict:
        return {
            "WIN_SCORE": self.WIN_SCORE,
            "LOSE_SCORE": self.LOSE_SCORE,
            "EXAEQUO_SCORE": self.EXAEQUO_SCORE,
            "LOOK_AHEADS": self.LOOK_AHEADS,
            "HEURISTIC_ROBOT": self.HEURISTIC_ROBOT,
            "HEURISTIC_OPPONENT": self.HEURISTIC_OPPONENT,
        }

    def apply_leaf_heuristic(self, grid, xCo, yCo) -> int:
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(xCo, yCo):
            if tile == self.robot_id:
                heuristic_score += self.HEURISTIC_ROBOT
            elif tile == self.get_id_opponent():
                heuristic_score += self.HEURISTIC_OPPONENT
        return heuristic_score

    def evaluate_leaf_move(self, grid, x):
        new_grid = grid.clone_with_move(x, self.robot_id)
        if new_grid.game_over() == self.robot_id:
            return 20
        else:
            return self.apply_leaf_heuristic(new_grid, x, grid.get_empty_top_index(x))

    def leaf_iteration(self, grid):
        moves_scores = []
        for move in grid.get_free_columns():
            moves_scores.append(self.evaluate_leaf_move(grid, move))
        return max(moves_scores)

    def max_iteration(self, grid, look_aheads_left) -> int:
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robot_id)
            if new_grid.game_over() == self.robot_id:
                return self.WIN_SCORE
            elif new_grid.game_over() == 'exaequo':
                moves_scores.append(self.EXAEQUO_SCORE)
            else:
                moves_scores.append(self.min_iteration(new_grid, look_aheads_left - 1))

        return max(moves_scores)

    # TODO merge max_ and min_ iteration methods?
    def min_iteration(self, grid, look_aheads_left) -> int:
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.get_id_opponent())
            if new_grid.game_over() == self.get_id_opponent():
                return self.LOSE_SCORE
            elif new_grid.game_over() == 'exaequo':
                moves_scores.append(self.EXAEQUO_SCORE)
            elif look_aheads_left == 2:
                moves_scores.append(self.leaf_iteration(new_grid))
            else:
                moves_scores.append(self.max_iteration(new_grid, look_aheads_left - 1))

        return min(moves_scores)

    def choose_move_with_minmax(self, grid) -> int:
        # Like max iteration except must remember move
        moves_scores = []

        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robot_id)
            # new_grid.game_over() -> IMPOSSIBLE
            if len(new_grid.get_free_columns()) == 0:  # check_if_immediate_win_possible does not check on exaequo
                moves_scores.append({'move': x, 'score': 0})
            else:
                moves_scores.append({'move': x, 'score': self.min_iteration(new_grid, self.LOOK_AHEADS - 1)})

        return max(moves_scores, key=lambda move: move['score'])['move']

    def choose_move(self, grid):
        if self.check_if_immediate_win_possible(grid):
            return self.check_if_immediate_win_possible(grid)['column']
        else:
            return self.choose_move_with_minmax(grid)
