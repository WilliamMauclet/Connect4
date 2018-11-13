from player import Player, X, Y, ZERO, get_other
import options, sequtils

const
    HEIGHT* = 6
    WIDTH* = 7
    HEURISTIC_FACTOR* = 10

type
    Column = array[HEIGHT, Player]
    Grid* = ref object of RootObj
        columns*:  array[WIDTH, Column]

proc new_grid*():Grid =
    return Grid(
        columns: [
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO]
        ]
    )


method `[]`* (self:Grid, x:int):Column {.base.} =
    result = self.columns[x]

method get_empty_top_index*(self:Grid, x:int):Option[int] {.base.} =
    for y in countup(0, HEIGHT-1):
        if self.columns[x][y] == ZERO:
            return some(y)
    return none(int)

method add_pawn*(self: var Grid, x:int, player:Player) {.base.} =
    let opt_y:Option[int] = self.get_empty_top_index(x)
    if opt_y.isSome():
        let y = opt_y.get()
        self.columns[x][y] = player
    else:
        raise newException(ArithmeticError, "Tried to add a pawn in a full column.")

method get_state_string_representation*(self:Grid):string {.base.} =
    var image = ""
    for x in countup(1, 15):
        image = image & "_"
    for y in countdown(5, 0):
        image = image & "\n|"
        for x in countup(0, 6):
            image = image & $self[x][y] & '|'
    result = image & "\n"

method print*(self:Grid) {.base.} =
    echo self.get_state_string_representation()

proc is_in_grid*(x:int, y:int): bool =
    var valid = 0 <= x and x < WIDTH and 0 <= y and y < HEIGHT
    return valid

proc has_four_in_repetition(sequence:openArray[Player]):Option[Player] =
    var 
        previous:Player = ZERO
        nr_repetitions:int = 0
    for new_value in sequence:
        if new_value == ZERO or new_value != previous:
            nr_repetitions = 0
        else:
            nr_repetitions += 1
            if nr_repetitions == 3:
                return some(previous)
        previous = new_value
    return none(Player)

method has_four_in_a_column*(self:Grid, x:int):Option[Player] {.base.} =
    return has_four_in_repetition(self[x])

method get_row(self:Grid, y:int):array[WIDTH, Player] =
    var row:array[WIDTH, Player]
    for x in 0..<WIDTH:
        row[x] = self[x][y]
    return row

method has_four_in_a_row*(self:Grid, y:int):Option[Player] {.base.} =
    return has_four_in_repetition(self.get_row(y))

method get_diagonal(self:Grid, x:int, y:int, y_incr:int):seq[Player] {.base.} =
    var 
        values:seq[Player] = @[]
        xCo = x
        yCo = y
    while is_in_grid(xCo, yCo):
        values &= self[xCo][yCo]
        xCo += 1
        yCo = yCo + y_incr
    return values   

method get_diagonal_down(self:Grid, x:int, y:int):seq[Player] {.base.} =
    return self.get_diagonal(x, y, -1)

method get_diagonal_up(self:Grid, x:int, y:int):seq[Player] {.base.} =
    return self.get_diagonal(x, y, 1)

method get_diagonals(self:Grid):seq[seq[Player]] {.base.} =
    return result # TODO implement and use in has_winner

method has_winner*(self:Grid):Option[Player] {.base.} =
    for x in 0..<WIDTH:
        var fiac = self.has_four_in_a_column(x)
        if fiac.isSome():
            return fiac
    for y in 0..<HEIGHT:
        var fiar = self.has_four_in_a_row(y)
        if fiar.isSome():
            return fiar
    for y in 0..<HEIGHT-3:
        var fiad = has_four_in_repetition(self.get_diagonal_up(0, y))
        if fiad.isSome():
            return fiad
    for y in 3..<HEIGHT:
        var fiad = has_four_in_repetition(self.get_diagonal_down(0, y))
        if fiad.isSome():
            return fiad
    for x in 0..<WIDTH-3:
        var fiad = has_four_in_repetition(self.get_diagonal_down(x, HEIGHT-1))
        if fiad.isSome():
            return fiad
    for x in 1..<WIDTH-3:
        var fiad = has_four_in_repetition(self.get_diagonal_up(x, 0))
        if fiad.isSome():
            return fiad

    return none(Player)

# TODO rename to 'get_open_column_indices'
method get_open_columns*(self:Grid):seq[int] {.base.} =
    result = @[]
    for x in 0..<WIDTH:
        if self[x][HEIGHT-1] == ZERO:
            result &= x
    return result

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


method heuristic*(self:Grid, player:Player):int {.base.} =
    # count {3*same}+{empty} in 4-seqs
    # multiply with 10
    # positive if player, negative if other player
    # same with 2+2empty in 4-seqs
    # but multiplied with 5
    var heur_sum = 0
    for x in self.get_open_columns():
        heur_sum += heuristic_full_seq(player, self[x])
    for y in 0..<HEIGHT:
        heur_sum += heuristic_full_seq(player, self.get_row(y))
    return heur_sum # TODO: diagonals!

method is_full*(self:Grid):bool {.base.} =
    return self.get_open_columns().len == 0

method clone(self:Grid):Grid {.base.} =
    var grid_clone = new_grid()
    for x in 0..<WIDTH:
        for y in 0..<HEIGHT:
            var pawn = self[x][y]
            if pawn == ZERO:
                break
            else:
                grid_clone.add_pawn(x, pawn)
    return grid_clone
    
method clone_for_move*(self:Grid, move:int, player:Player):Grid {.base.} =
    var grid_clone = self.clone()
    grid_clone.add_pawn(move, player)
    return grid_clone

method game_over*(self:Grid): bool {.base.} =
    return self.has_winner().isSome()