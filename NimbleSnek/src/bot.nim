from player import Player
import grid

type
    Bot* = ref object of RootObj
        id : Player

proc new_bot*(id: Player): Bot = 
    return Bot(id: id)

method choose_move*(self: Bot, grid: Grid): int =
    return 2