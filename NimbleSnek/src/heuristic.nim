import sequtils
import player, grid

const HEURISTIC_FACTOR* = 10

proc heuristic_4_seq(player:Player, sequence:openArray[Player]):int =
    var 
        factor:int
        heuristic_val:int
    if sequence.contains(player) and sequence.contains(get_other(player)):
        return 0
    if not sequence.contains(player) and not sequence.contains(get_other(player)):
        return 0
    if sequence.contains(player):
        return sequence.count(player)-1 * HEURISTIC_FACTOR
    else:
        return sequence.count(get_other(player))-1 * HEURISTIC_FACTOR * -1
    

proc heuristic_full_seq(player:Player, sequence:openArray[Player]):int =
    var heur_sum = 0
    for x in 0..sequence.len-4:
        heur_sum += heuristic_4_seq(player, sequence[x..x+3])
    return heur_sum


proc heuristic*(self:Grid, player:Player):int =
    var heur_sum = 0
    for sequence in self.get_sequences():
        heur_sum += heuristic_full_seq(player, sequence)
    return heur_sum