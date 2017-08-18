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

            moves_scores.append(self._alpha_beta(new_grid, self.depth - 1, -inf, +inf, False, x))

        # TODO shuffle moves_scores? => makes it less re-playable!

        best_move = max(moves_scores, key=lambda move: move['score'])

        minmax_tree = {
            'score': best_move['score'],
            'move': best_move['move'],
            'next': moves_scores
        }
        import logging
        logging.log(logging.DEBUG, minmax_tree)

        return best_move

    # TODO return {'score': int, 'move': int, 'next':[]}
    def _alpha_beta(self, grid, depth: int, alpha: int, beta: int, max_not_min: bool, move: int) -> {}:
        if depth == 0:
            return {'score': self._apply_leaf_heuristic(grid), 'move': move}
        if grid.game_over() != -1:
            if grid.game_over() == 'exaequo':
                return {'score': self.exaequo_score, 'move': move}
            if grid.game_over() == self.bot_id:
                return {'score': self.win_score, 'move': move}
            if grid.game_over():  # opponent has won
                return {'score': self.lose_score, 'move': move}

        next_moves = {}
        if max_not_min:
            v = {'score': -inf}
            # TODO use generator get_free_columns()
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move(x, self.bot_id)
                move_score = self._alpha_beta(new_grid, depth - 1, alpha, beta, False, x)
                next_moves[x] = move_score
                v = max(v, move_score, key=lambda l: l['score'])
                alpha = max(alpha, v['score'])
                if beta <= alpha:
                    break

            v['next'] = next_moves
            return v
        else:
            v = {'score': +inf}
            for x in grid.get_free_columns():
                new_grid = grid.clone_with_move_opponent(x, self.bot_id)
                move_score = self._alpha_beta(new_grid, depth - 1, alpha, beta, True, x)
                next_moves[x] = move_score
                v = min(v, move_score, key=lambda l: l['score'])
                beta = min(beta, v['score'])
                if beta <= alpha:
                    break
            v['next'] = next_moves
            return v

    def _apply_leaf_heuristic(self, grid) -> int:
        x_co = grid.get_last_move()[0]
        y_co = grid.get_filled_top_index(x_co)
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(x_co, y_co):
            if tile == self.bot_id:
                heuristic_score += self.heuristic_bot
            elif self._is_id_opponent(tile):
                heuristic_score += self.heuristic_opponent
        return heuristic_score
