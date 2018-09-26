import grid, bot, player
from strutils import parseInt

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

    var id_index = 0
    while not grid.game_over():
        grid.print()
        accept_move(grid, id_index, bot)
        id_index = (id_index+1) mod 2 
        # TODO
        
proc accept_move(grid: var Grid, player_index: int, bot: Bot) =
    var column: int
    if bool(player_index):
        column = bot.choose_move(grid)
    else:
        column = accept_human_move(grid)
    echo PLAYER_INVOCS[player_index] & " played column: " & $(column+1)
    grid.add_pawn(column, PLAYERS[player_index])

proc accept_human_move(grid: Grid): int =
    # TODO
    echo "Choose a move:"
    return  parseInt(stdin.readLine())

start()