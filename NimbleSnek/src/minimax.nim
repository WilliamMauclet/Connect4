import tables
import grid 
import player

from random import nil

const DEPTH = 7
const INFINITY = 1_000_000_000

proc end_game_score(max_not_min:bool, depth:int):int =
    if max_not_min:
        # here the game is won when it's a max turn: hence negative
        return -5*depth # depth decreases: the sooner, the higher 
    else:
        return 5*depth

proc alpha_beta(player:Player, grid:Grid, depth:int, prev_alpha:int, prev_beta:int, max_not_min:bool):int =
    # grid.print()
    if grid.game_over():
        return end_game_score(max_not_min, depth)

    if depth == 0 or grid.is_full(): # TODO: or grid is a terminal grid 
        # TODO: if you get here, then there hasn't been a winner by the time we're at depth 0
        return 0 # TODO: the heuristic value in grid
    if max_not_min:
        var 
            value = -INFINITY # -infinite
            alpha = prev_alpha
        for move in grid.get_open_columns():
            value = max(value, alpha_beta(get_other(player), grid.clone_for_move(move, player), depth-1, alpha, prev_beta, false))
            alpha = max(alpha, value)
            if alpha >= prev_beta:
                break # beta cut-off
        return value
    else:
        var
            value = INFINITY # +infinite
            beta = prev_beta
        for move in grid.get_open_columns():
            value = min(value, alpha_beta(get_other(player), grid.clone_for_move(move, player), depth-1, prev_alpha, beta, true))
            beta = min(beta, value)
            if prev_alpha >= beta :
                break # alpha cut-off
        return value

#(* Initial call *)
#alphabeta(origin, depth, −∞, +∞, TRUE)

proc find_best_move*(grid:Grid, player:Player):int =
    var 
        best_move = -1
        best_score = -INFINITY

    for x in grid.get_open_columns():
        var move_result = alpha_beta(get_other(player), grid.clone_for_move(x, player), DEPTH-1, -INFINITY, INFINITY, false)
        
        echo "move " & $x & " gives a score of " & $move_result

        if move_result > best_score:
            best_move = x
            best_score = move_result 
    
    if best_move == -1:
        echo "no best move found by bot!"
        return random.random(7)
    else:
        return best_move
