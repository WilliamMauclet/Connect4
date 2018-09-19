from math import inf
import logging

from hispida.bots.FirstOrderBot import FirstOrderBot


class MinmaxBot(FirstOrderBot):
    """Applies a minmax algorithm. Only 2n+1 iterations considered. should only work for values 2n+1."""

    def __init__(self, bot_id, depth=5, win_score=20, lose_score=-20, exaequo_score=0,
                 heuristic_bot=1, heuristic_opponent=-3):
        super().__init__(bot_id)
        self.depth = depth
        self.win_score = win_score
        self.lose_score = lose_score
        self.exaequo_score = exaequo_score
        self.heuristic_bot = heuristic_bot
        self.heuristic_opponent = heuristic_opponent

    def set_heuristic_params(self, heuristic_bot, heuristic_opponent):
        self.heuristic_bot = heuristic_bot
        self.heuristic_opponent = heuristic_opponent

    def get_configuration(self) -> dict:
        return self.__dict__

    def get_descriptor(self) -> str:
        descriptor = "{}:{}" + "/{}" * 5
        return descriptor.format(
            self.__class__.__name__,
            self.depth,
            self.win_score,
            self.lose_score,
            self.exaequo_score,
            self.heuristic_bot,
            self.heuristic_opponent
        )

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
        moves_scores = {}
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.bot_id)
            moves_scores[x] = self._alpha_beta(new_grid, self.depth - 1, -inf, +inf, True)

        best_move = max(moves_scores, key=lambda move: moves_scores[move]['score'])

        self._log_minmax_tree(best_move, grid, moves_scores)

        return best_move

    def _log_minmax_tree(self, best_move, grid, moves_scores):
        minmax_tree = {
            'best_score': moves_scores[best_move]['score'],
            'best_move': best_move,
            'moves': moves_scores
        }
        logging.log(logging.DEBUG, minmax_tree)
        if minmax_tree['best_score'] is -1:
            # TODO log
            print("Whatever I (={}) do, I will lose within {} turns with this board \n{}".format(
                self.bot_id,
                self.depth / 2,
                grid.get_state_string_representation()))
        if all(x['score'] for x in moves_scores.values()):
            logging.log(logging.DEBUG,
                        "All moves are as good for this grid:\n " + grid.get_state_string_representation())

    def _alpha_beta(self, grid, depth, alpha, beta, min_not_max):
        if depth == 0:
            return {'score': self._apply_leaf_heuristic(grid), 'depth': 0}
        if grid.game_over():
            return self._end_game_score(grid, depth)

        next_moves = {}
        v = {'score': +inf if min_not_max else -inf}
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.bot_id, for_opponent=min_not_max)
            move_score = self._alpha_beta(new_grid, depth - 1, alpha, beta, not min_not_max)
            next_moves[x] = move_score
            v, alpha, beta = self._update_values(v, alpha, beta, move_score, min_not_max)
            if beta <= alpha:
                break

        return {'score': v['score'], 'depth': depth, 'next': next_moves}

    def _end_game_score(self, grid, depth):
        if grid.game_over() == 'exaequo':
            return {'score': self.exaequo_score, 'depth': depth}
        if grid.game_over() == self.bot_id:
            return {'score': self.win_score, 'depth': depth}
        if grid.game_over():  # opponent has won
            return {'score': self.lose_score, 'depth': depth}

    @staticmethod
    def _update_values(v, alpha, beta, move_score, min_not_max):
        if min_not_max:
            v = min(v, move_score, key=lambda l: l['score'])
            beta = min(beta, v['score'])
        else:
            v = max(v, move_score, key=lambda l: l['score'])
            alpha = max(alpha, v['score'])

        return v, alpha, beta

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
