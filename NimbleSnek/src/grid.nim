from player import Player, X, Y, ZERO, get_other
import options, sequtils

const
    HEIGHT* = 6
    WIDTH* = 7

type
    Grid* = array[WIDTH, array[HEIGHT, Player]]

proc new_grid*():Grid =
    return [
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO]
        ]

proc get_empty_top_index*(self:Grid, x:int):Option[int] =
    for y in countup(0, HEIGHT-1):
        if self[x][y] == ZERO:
            return some(y)
    return none(int)

proc add_pawn*(self: var Grid, x:int, player:Player) =
    let opt_y:Option[int] = self.get_empty_top_index(x)
    if opt_y.isSome():
        let y = opt_y.get()
        self[x][y] = player
    else:
        raise newException(ArithmeticError, "Tried to add a pawn in a full column.")

proc get_state_string_representation*(self:Grid):string =
    var image = ""
    for x in countup(1, 15):
        image = image & "_"
    for y in countdown(5, 0):
        image = image & "\n|"
        for x in countup(0, 6):
            image = image & $self[x][y] & '|'
    result = image & "\n"

proc print*(self:Grid) =
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

proc has_four_in_a_column*(self:Grid, x:int):Option[Player] =
    return has_four_in_repetition(self[x])

proc get_columns(self:Grid):array[WIDTH,array[HEIGHT,Player]] =
    var columns:array[WIDTH,array[HEIGHT,Player]]
    for x in 0..<WIDTH:
        columns[x] = self[x]
    return columns

proc get_row(self:Grid, y:int):array[WIDTH, Player] =
    var row:array[WIDTH, Player]
    for x in 0..<WIDTH:
        row[x] = self[x][y]
    return row

proc has_four_in_a_row*(self:Grid, y:int):Option[Player] =
    return has_four_in_repetition(self.get_row(y))

proc get_rows(self:Grid):array[HEIGHT,array[WIDTH, Player]] =
    var rows:array[HEIGHT,array[WIDTH, Player]]
    for y in 0..<HEIGHT:
        rows[y] = self.get_row(y)
    return rows

proc get_diagonal(self:Grid, x:int, y:int, y_incr:int):seq[Player] =
    var 
        values:seq[Player] = @[]
        xCo = x
        yCo = y
    while is_in_grid(xCo, yCo):
        values &= self[xCo][yCo]
        xCo += 1
        yCo = yCo + y_incr
    return values   

proc get_diagonal_down*(self:Grid, x:int, y:int):seq[Player] =
    return self.get_diagonal(x, y, -1)

proc get_down_diagonals(self:Grid):array[6,seq[Player]] =
    var 
        down_diagonals: array[6, seq[Player]]
        index = 0
    for y in 3..<HEIGHT:
        down_diagonals[index] = self.get_diagonal_down(0, y)
        index += 1
    for x in 1..<WIDTH-3:
        down_diagonals[index] = self.get_diagonal_down(x, HEIGHT-1)
        index += 1
    return down_diagonals

proc get_diagonal_up*(self:Grid, x:int, y:int):seq[Player] =
    return self.get_diagonal(x, y, 1)

proc get_up_diagonals(self:Grid):array[6,seq[Player]] =
    var 
        up_diagonals: array[6, seq[Player]]
        index = 0
    for y in 0..<HEIGHT-3:
        up_diagonals[index] = self.get_diagonal_up(0, y) 
        index += 1
    for x in 1..<WIDTH-3:
        up_diagonals[index] = self.get_diagonal_up(x, 0)
        index += 1
    return up_diagonals

proc get_diagonals(self:Grid):array[12,seq[Player]] =
    var 
        diagonals:array[12,seq[Player]]
        index = 0
    let
        up_diagonals = self.get_up_diagonals()
        down_diagonals = self.get_down_diagonals()
    for index in 0..<6:
        diagonals[index] = up_diagonals[index]
    for index in 6..<12:
        diagonals[index] = down_diagonals[index-6]
    return diagonals

proc get_sequences*(self:Grid):array[25,seq[Player]] =
    let 
        diagonals = self.get_diagonals()
        columns = self.get_columns()
        rows = self.get_rows()
    var 
        seqs:array[25,seq[Player]]
        index = 0
    for column in columns:
        seqs[index] = @column
        index += 1
    for row in rows:
        seqs[index] = @row
        index += 1
    for diagonal in diagonals:
        seqs[index] = diagonal
        index += 1
    return seqs


proc has_winner*(self:Grid):Option[Player] =
    for sequence in self.get_sequences():
        var fias = has_four_in_repetition(sequence)
        if fias.isSome():
            return fias

    return none(Player)

proc get_open_column_indices*(self:Grid):seq[int] =
    result = @[]
    for x in 0..<WIDTH:
        if self[x][HEIGHT-1] == ZERO:
            result &= x
    return result

proc is_full*(self:Grid):bool =
    return self.get_open_column_indices().len == 0

proc clone(self:Grid):Grid =
    var grid_clone = new_grid()
    for x in 0..<WIDTH:
        for y in 0..<HEIGHT:
            var pawn = self[x][y]
            if pawn == ZERO:
                break
            else:
                grid_clone.add_pawn(x, pawn)
    return grid_clone
    
proc clone_for_move*(self:Grid, move:int, player:Player):Grid =
    var grid_clone = self.clone()
    grid_clone.add_pawn(move, player)
    return grid_clone

proc game_over*(self:Grid): bool =
    return self.has_winner().isSome()