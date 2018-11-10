type Player* = enum
    ZERO = "_", X = "x", Y = "y"

proc get_other*(player:Player):Player =
    if player == X:
        return Y
    if player == Y:
        return X
    raise new(Exception)