import unittest, grid, player, options, strutils

suite "Grid":
  test "get_empty_top_index":
    check new_grid().get_empty_top_index(4).get() == 0

  # TODO
  # test "get_empty_top_index with full column":
  #   check new_grid().get_empty_top_index(4).get() == 5

  test "check initialization":
    let grid = new_grid()
    check grid.columns[4][2] == ZERO
  
  test "check column getter":
    check new_grid()[4][3] == ZERO

  test "add_pawn":
    var grid = new_grid()
    grid.add_pawn(2, X)
    check grid[2][0] == X

  test "add_pawn twice":
    var grid = new_grid()
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    check grid[2][0] == Y
    check grid[2][1] == X

  test "get_state_string_representation":
    var grid = new_grid()
    grid.add_pawn(2, X)
    check "x" in grid.get_state_string_representation()
    check (not("y" in grid.get_state_string_representation()))

  test "game_over":
    check new_grid().game_over() == false

  test "test":
    check bool(0) == false
    check bool(1) == true
    echo "hey"
    echo("hey")