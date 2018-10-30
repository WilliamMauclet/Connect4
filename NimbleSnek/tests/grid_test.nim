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

  test "has_four_in_a_column #none":
    var grid = new_grid()
    check grid.has_four_in_a_column(2).isNone()

  test "has_four_in_a_column #not_enough":
    var grid = new_grid()
    for i in 0..2:
      grid.add_pawn(2, X)
    check grid.has_four_in_a_column(2).isNone()

  test "has_four_in_a_column #enough":
    var grid = new_grid()
    for i in 0..3:
      grid.add_pawn(2, X)
    check grid.has_four_in_a_column(2).isSome()
    check grid.has_four_in_a_column(2).get() == X

  test "has_four_in_a_row #none":
    var grid = new_grid()
    check grid.has_four_in_a_row(0).isNone()

    test "has_four_in_a_row #interleave":
      var grid = new_grid()
      grid.add_pawn(3, Y)
      grid.add_pawn(3, X)
      grid.add_pawn(3, Y)
      grid.add_pawn(3, Y)
      grid.add_pawn(3, Y)
      check grid.has_four_in_a_row(0).isNone()
      
  test "has_four_in_a_row #not_enough":
    var grid = new_grid()
    for x in 2..4:
      grid.add_pawn(x, Y)
    check grid.has_four_in_a_row(0).isNone()
  
  test "has_four_in_a_row #enough":
    var grid = new_grid()
    for x in 2..5:
      grid.add_pawn(x, Y)
    check grid.has_four_in_a_row(0).isSome()
    check grid.has_four_in_a_row(0).get() == Y
  
  test "get_diagonal_down":
    var grid = new_grid()
    grid.add_pawn(5, X)
    check grid.get_diagonal_down(0, 5) == @[ZERO, ZERO, ZERO, ZERO, ZERO, X]

  test "get_diagonal_up #complex":
    var grid = new_grid()
    grid.add_pawn(0, Y)
    grid.add_pawn(1, Y)
    grid.add_pawn(1, X)
    check grid.get_diagonal_up(0, 0) == @[Y, X, ZERO, ZERO, ZERO, ZERO]

  test "has_winner (no)":
    var grid = new_grid()
    grid.add_pawn(0, X)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    check grid.has_winner().isNone()
  
  test "has_winner (Y,up)":
    var grid = new_grid()
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    check grid.has_winner().get() == Y

  test "has_winner (X,right)":
    var grid = new_grid()
    grid.add_pawn(2, X)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    grid.add_pawn(5, X)
    check grid.has_winner().get() == X

  test "has_winner (X,diagonal up)":
    var grid = new_grid()
    grid.add_pawn(1, X)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, X)
    grid.add_pawn(4, X)
    check grid.has_winner().get() == X

  test "has_winner (X,diagonal down)":
    var grid = new_grid()
    grid.add_pawn(1, X)
    grid.add_pawn(1, Y)
    grid.add_pawn(1, X)
    grid.add_pawn(1, X)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    check grid.has_winner().get() == X
 
  test "game_over":
    check new_grid().game_over() == false

  test "test":
    check bool(0) == false
    check bool(1) == true
    check pred(2) == 1
    check succ(3) == 4
    echo "hey"
    echo("hey")
  
  test "sequence":
    var sequ = @[9, 9, 9]
    for i in sequ:
      echo i