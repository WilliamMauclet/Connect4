from math import inf

from FirstOrderBot import FirstOrderBot


class MinmaxBot(FirstOrderBot):
    """Applies a minmax algorithm. Only 2n+1 iterations considered. should only work for values 2n+1."""

    def __init__(self, bot_id,
                 win_score=20, lose_score=-1, exaequo_score=0,
                 heuristic_bot=2, heuristic_opponent=1, depth=5):
        super().__init__(bot_id)
        self.win_score = win_score
        self.lose_score = lose_score
        self.exaequo_score = exaequo_score
        self.heuristic_bot = heuristic_bot
        self.heuristic_opponent = heuristic_opponent
        self.depth = depth

    def set_heuristic_params(self, heuristic_bot, heuristic_opponent):
        self.heuristic_bot = heuristic_bot
        self.heuristic_opponent = heuristic_opponent

    def get_configuration(self) -> dict:
        # TODO: automatically iterate over fields of instance?
        return {
            "WIN_SCORE": self.win_score,
            "LOSE_SCORE": self.lose_score,
            "EXAEQUO_SCORE": self.exaequo_score,
            "DEPTH": self.depth,
            "HEURISTIC_BOT": self.heuristic_bot,
            "HEURISTIC_OPPONENT": self.heuristic_opponent,
        }

    # TODO pretty-print to debug
    def choose_move(self, grid) -> int:
        # First two checks speed up and make bot better.
        if self._check_if_immediate_win_possible(grid):
            return self._check_if_immediate_win_possible(grid)['column']
        elif grid.get_nr_moves_left() == 1:
            return next(grid.get_free_columns())
        else:
            return self._choose_move_with_minmax(grid)

    def _choose_move_with_minmax(self, grid) -> int:
        # Like max iteration except must remember move.
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.bot_id)

            moves_scores.append({'move': x, 'score': self._alpha_beta(new_grid, self.depth - 1, -inf, +inf, False)})

        # TODO shuffle moves_scores? => makes it less re-playable!
        return max(moves_scores, key=lambda move: move['score'])['move']

    # TODO return [{'score': , 'move': }, previous_moves_with_score]
    def _alpha_beta(self, grid, depth: int, alpha: int, beta: int, max_not_min: bool) -> int:
        if depth == 0:
            return self._apply_leaf_heuristic(grid)
        if grid.game_over() != -1:
            if grid.game_over() == 'exaequo':
                return self.exaequo_score
            if grid.game_over() == self.bot_id:
                return self.win_score
            if grid.game_over():  # opponent has won
                return self.lose_score

        if max_not_min:
            v = -inf
            # TODO use generator get_free_columns()
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move(x, self.bot_id)
                v = max(v, self._alpha_beta(new_grid, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        else:
            v = +inf
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move_opponent(x, self.bot_id)
                v = min(v, self._alpha_beta(new_grid, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return v

    def _apply_leaf_heuristic(self, grid) -> int:
        x_co = grid.get_last_move()[0]
        y_co = grid.get_empty_top_index(x_co) - 1
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(x_co, y_co):
            if tile == self.bot_id:
                heuristic_score += self.heuristic_bot
            elif self._is_id_opponent(tile):
                heuristic_score += self.heuristic_opponent
        return heuristic_score
