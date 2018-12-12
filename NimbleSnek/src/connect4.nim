import grid, bot, player
from strutils import parseInt, isDigit

# forward declaration
proc accept_move(grid: var Grid, player_index: int, bot: Bot)
proc accept_human_move(grid: Grid): int

const 
    PLAYERS = [X, Y]
    PLAYER_INVOCS = ["You", "Bot"]

proc start() =
    var grid = new_grid()
    echo "\nWelcome to a new game of Connect 4\n"
    var bot = new_bot(Y)

    var id_index = 1
    grid.print()
    while not grid.game_over():
        id_index = (id_index+1) mod 2 
        accept_move(grid, id_index, bot)
        grid.print()
    
    echo PLAYER_INVOCS[id_index] & " won, congrats!\n"
        
proc accept_move(grid: var Grid, player_index: int, bot: Bot) =
    var column: int
    if bool(player_index):
        column = bot.choose_move(grid)
    else:
        column = accept_human_move(grid)
    echo PLAYER_INVOCS[player_index] & " played column: " & $(column+1)
    grid.add_pawn(column, PLAYERS[player_index])

proc is_valid_input(grid:Grid, input:TaintedString):bool =
    return input.isDigit() and 
        0 < parseInt(input) and 
        parseInt(input) <= 7 and grid.get_open_column_indices.contains(parseInt(input)-1)

proc accept_human_move(grid: Grid): int =
    echo "Choose a move:"

    var input = stdin.readLine()
    while not(is_valid_input(grid, input)):
        echo "Please choose a correct move from " & $grid.get_open_column_indices()
        input = stdin.readLine()
    return parseInt(input) - 1

start()
