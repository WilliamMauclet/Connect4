from player import Player, X, Y, ZERO
import options

const
    HEIGHT = 6
    WIDTH = 7

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

method `[]`* (self: Grid, x: int): Column {.base.} =
    result = self.columns[x]

method get_empty_top_index*(self: Grid, x: int): Option[int] {.base.} =
    for y in countup(0, HEIGHT-1):
        if self.columns[x][y] == ZERO:
            return some(y)
    return none(int)

method add_pawn*(self: var Grid, x: int, player: Player) {.base.} =
    let opt_y: Option[int] = self.get_empty_top_index(x)
    if opt_y.isSome():
        let y = opt_y.get()
        self.columns[x][y] = player
    else:
        raise newException(ArithmeticError, "Tried to add a pawn in a full column.")

method get_state_string_representation*(self: Grid): string {.base.} =
    var image = ""
    for x in countup(1, 15):
        image = image & "_"
    for y in countdown(5, 0):
        image = image & "\n|"
        for x in countup(0, 6):
            image = image & $self[x][y] & '|'
    result = image & "\n"

method print*(self: Grid) {.base.} =
    echo self.get_state_string_representation()

method game_over*(self: Grid): bool {.base.}=
    result = false

method has_four_in_a_column*(self: Grid, x: int): Option[Player] {.base.} =
    var 
        previous: Player = ZERO
        nr_repetitions: int = 0
    for y in 0..<HEIGHT:
        var new_value = self[x][y] 
        if new_value == ZERO:
            return none(Player)
        elif previous == new_value:
            nr_repetitions += 1
            if nr_repetitions == 4:
                return some(previous)
        else:
            nr_repetitions = 0
        previous = new_value
    return none(Player)

method has_four_in_a_row*(self: Grid, y: int): Option[Player] {.base.} =
    var 
        previous: Player = ZERO
        nr_repetitions: int = 0
    for x in 0..<WIDTH:
        var new_value = self[x][y] 
        if new_value == ZERO or new_value != previous:
            nr_repetitions = 0
        else:
            nr_repetitions += 1
            if nr_repetitions == 3:
                return some(previous)
        previous = new_value
    return none(Player)

