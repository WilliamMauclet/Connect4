from player import Player
import grid
from random import nil

type
    Bot* = ref object of RootObj
        id : Player

proc new_bot*(id: Player): Bot = 
    return Bot(id: id)

method choose_move*(self: Bot, grid: Grid): int {.base.} =
    return random.random(7)